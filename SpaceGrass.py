import numpy as np
import math
from sys import argv

#math.pi = 3.14

Population = 8
Oxi_Cost = 7
Fuel_Cost = 10

# Считаю Kp.
# Эта таблица - константная, она не зависит от каких-то параметров.
# Она используется в половине рассчётов дальше.
Kp = np.empty([21, 61], dtype=np.float64)
for i in range(21):  # T
    for j in range(61):  # Oxi
        Kp[i, j] = -math.pi / 2 + (i + j * 0.5) / 40 * math.pi
Kp = np.sin(Kp)


def Cvt_T2Fuel(T):
    """ Рассчитывает затраты ядерного топлива на поддержание заданной темперартуры.
    """
    Energy = 0
    for i in range(T+1):
        Energy += i
    # print(Energy)

    if Energy - Energy // 11 > 0:
        Fuel = Energy // 11 + 1
    else:
        Fuel = Energy // 11
    return Fuel


def Find_Economy_T_and_Oxi(Pop, NeedPop):
    """ Функция находит наиболее экономически выгодные комбинации ТЕМПЕРАТУРЫ и КИСЛОРОДА
        для роста популяции на заданное значение.

        Входные данные: текущая популяция, необходимая популяция
        Выходные данные: список списков подходящих вариантов
                         [[T, Oxi, Kp]
                          [T, Oxi, Kp]
                          [T, Oxi, Kp]]
    """
    good_T_Oxi = []
    for i in range(21):  # T
        for j in range(61):  # Oxi
            NewPop = (Pop + Pop * Kp[i, j]) // 1
            if NewPop == NeedPop:
                good_T_Oxi.append([i, j])


    economy_T_Oxi = []
    MinCoast = 1000000000000000
    for param in good_T_Oxi:  # переводим всё в цену и берём минимум
        # param[0]  # Температура
        # param[1]  # Кислород
        AllCoast = Cvt_T2Fuel(param[0])*Fuel_Cost  # учли стоимость топлива
        AllCoast += param[1]*Pop*Oxi_Cost  # учли стоимость кислорода
        if AllCoast < MinCoast:
            economy_T_Oxi = [param[0], param[1], AllCoast]
            MinCoast = AllCoast
        elif AllCoast == MinCoast:
            economy_T_Oxi.append([param[0], param[1], AllCoast])

    return economy_T_Oxi



def DayForGrow(NeedPop):
    """Считает число дней необходимых на культивацию
       Входные данные - количество SP для отгрузки"""

    if NeedPop <= 8:
        day = 1
    else:
        day = math.log2((NeedPop+8)/8)
    return day



Vmax = 2
W = 80


def GrowDist(day):
    """
    Считает пройденную дистанцию при росте с 1 коэфиициентом за заданное число дней
    """
    GrowDist_var = 0
    Pop = 8
    for i in range(day):
        M = 192 + (Pop * 1)  # умножаю на одну тонну
        V = Vmax * (W/80)*(200/M)
        Pop *= 2
        Dist = V * 1  # на день умножаю, скорость в дистанцию перевожу
        GrowDist_var += Dist
    return GrowDist_var



def NoGrowDay(Dist, GrowDay):
    """ Счиает число дней без роста.
        Входящие данные: Дистанция до след точки и число дней с ростом.
    """
    DistNoGrow = Dist - GrowDist(GrowDay)
    NoGrowDay_var = DistNoGrow / Vmax
    if NoGrowDay_var % 1 > 0:
        NoGrowDay_var += 1
    return NoGrowDay_var


def ResNoGrowDay(NoGrowDay_var):
    """ Считает ресурсы затрачиваемые за все дни без культивирования SH.
        Входящие данные: количество дней без культивации.
    """
    Pop = 8
    AllNoGrowCost = 0
    AllNoGrowFuel = 0
    AllNoGrowOxi = 0
    for i in range(NoGrowDay_var):
        list_var = Find_Economy_T_and_Oxi(8, 8)
        T = list_var[0]
        FuelGrow = Cvt_T2Fuel(T)
        Oxi = list_var[1]*Pop
        CostGrowRes = list_var[2]
        AllNoGrowCost += (CostGrowRes + 80*Fuel_Cost)
        AllNoGrowFuel += (FuelGrow + 80)  #
        AllNoGrowOxi += Oxi
    return AllNoGrowFuel, AllNoGrowOxi, AllNoGrowCost


def ResGrowDay(GrowDay_var):
    """ Считает ресурсы затрачиваемые за все дни C культивацией SH.
        Входящие данные: количество дней с культивацией.
    """
    Pop = 8
    AllGrowCost = 0
    AllGrowFuel = 0
    AllGrowOxi = 0
    for i in range(GrowDay_var):
        list_var = Find_Economy_T_and_Oxi(Pop, Pop*2)
        if len(list_var) != 3:
            list_var = list_var[0]
        T = list_var[0]

        FuelGrow = Cvt_T2Fuel(T)
        Oxi = list_var[1] * Pop
        CostGrowRes = list_var[2]
        AllGrowCost += (CostGrowRes + 80 * Fuel_Cost)
        AllGrowFuel += (FuelGrow + 80)
        AllGrowOxi += Oxi
        Pop *= 2
    return AllGrowFuel, AllGrowOxi, AllGrowCost


def ResGrowOneDay(NeedPop):
    """ Считает ресурсы затрачиваемые за один день культивацией SH,
        для случаев когда итоговая популяция от [0 до 16)
        Входящие данные: Значение популяции в конце дня.
    """
    Pop = 8
    list_var = Find_Economy_T_and_Oxi(Pop, NeedPop)
    if len(list_var) != 3:
#        print("Have sone variant")
#        print(list_var)
#        print("Use first variant")
        list_var = list_var[0]
    T = list_var[0]
    FuelGrow = Cvt_T2Fuel(T)
    Oxi = list_var[1] * Pop
    CostGrowRes = list_var[2]
    AllGrowCost = (CostGrowRes + 80 * Fuel_Cost)
    AllGrowFuel = (FuelGrow + 80)
    AllGrowOxi = Oxi

    return AllGrowFuel, AllGrowOxi, AllGrowCost

def main(Fly_Dist, SP_ForClient):
    if SP_ForClient == 0:  #Если ничего не надо выращивать
        day_grow_var = 0
    elif SP_ForClient <= 7:  # если надо отгрузить мало - меньше 8
        day_grow_var = 1
        day_no_grow_var = int(NoGrowDay(Fly_Dist, day_grow_var))  # считает число дней, которое летим до культивации
        # print("Day Not Grow: " + str(day_no_grow_var) + "     Day for Grow: " + str(day_grow_var))
        AllFuel, All_Oxi, All_cost = ResNoGrowDay(day_no_grow_var)  # выводим ресурсы и стоимость для дней без культивации
        # print("Cultivation Start")
        var1, var2, var3 = ResGrowOneDay(SP_ForClient+8)
        AllFuel += var1
        All_Oxi += var2
        All_cost += var3


    else:  # условно нормальные значения отгрузки 8, 24, 56 ....
        day_grow_var = int(DayForGrow(SP_ForClient))  # столько дней надо на культивацию
        day_no_grow_var = int(NoGrowDay(Fly_Dist, day_grow_var))  # считает число дней, которое летим до культивации
        AllFuel, All_Oxi, All_cost = ResNoGrowDay(day_no_grow_var)  # выводим ресурсы и стоимость для дней без культивации
        var1, var2, var3 = ResGrowDay(day_grow_var)
        AllFuel += var1
        All_Oxi += var2
        All_cost += var3
    return AllFuel, All_Oxi, All_cost, day_grow_var+day_no_grow_var
 

if __name__ == '__main__':

    Fly_Dist = int(argv[1])
    SP_ForClient = int(argv[2]) - 8
    print(main(Fly_Dist, SP_ForClient))
