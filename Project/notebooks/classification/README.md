# [Дефекты при изготовлении стальных пластин](http://archive.ics.uci.edu/ml/datasets/Steel+Plates+Faults) ([link2](https://github.com/makinarocks/awesome-industrial-machine-datasets/tree/master/data-explanation/Steel%20Plates%20Faults))

Набор данных о неисправностях стальных пластин, классифицированных на 7 различных типов.

Набор данных содержит 7 классов и 27 признаков, которые описывают неисправность: (местоположение, размер,...) и тип неисправности (один из 7: 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults')

## (Предположительные) назначения признаков

| Имя                     | Тип   | Описание                                         |
| ----------------------- | ----- | ------------------------------------------------ |
| 'X_Minimum'             | int   | Минимальная ширина дефекта                       |
| 'X_Maximum'             | int   | Максимальная ширина дефекта                      |
| 'Y_Minimum'             | int   | Минимальная высота дефекта                       |
| 'Y_Maximum'             | int   | Максимальная высота дефекта                      |
| 'Pixels_Areas'          | int   | ???                                              |
| 'X_Perimeter'           | int   | Периметр по X                                    |
| 'Y_Perimeter'           | int   | Периметр по Y                                    |
| 'Sum_of_Luminosity'     | int   | Суммарный коэффициент светимости (освещения?)    |
| 'Minimum_of_Luminosity' | int   | Минимальный коэффициент светимости (освещения?)  |
| 'Maximum_of_Luminosity' | int   | Максимальный коэффициент светимости (освещения?) |
| 'Length_of_Conveyer'    | int   | Длина конвейера                                  |
| 'TypeOfSteel_A300'      | bool  | Соответствие стали классу A-II (A300)            |
| 'TypeOfSteel_A400'      | bool  | Соответствие стали классу A-III (A400)           |
| 'Steel_Plate_Thickness' | int   | Толщина стальной пластины                        |
| 'Edges_Index'           | float | ???                                              |
| 'Empty_Index'           | float | ???                                              |
| 'Square_Index'          | float | ???                                              |
| 'Outside_X_Index'       | float | ???                                              |
| 'Edges_X_Index'         | float | ???                                              |
| 'Edges_Y_Index'         | float | ???                                              |
| 'Outside_Global_Index'  | float | ???                                              |
| 'LogOfAreas'            | float | ???                                              |
| 'Log_X_Index'           | float | ???                                              |
| 'Log_Y_Index'           | float | ???                                              |
| 'Orientation_Index'     | float | ???                                              |
| 'Luminosity_Index'      | float | ???                                              |
| 'SigmoidOfAreas'        | float | ???                                              |
| 'Pastry'                | bool  | ???                                              |
| 'Z_Scratch'             | bool  | Дефект металла: царапины 1                       |
| 'K_Scatch'              | bool  | Дефект металла: царапины 2                       |
| 'Stains'                | bool  | Дефект металла: ржавчина                         |
| 'Dirtiness'             | bool  | Дефект металла: загрязнение                      |
| 'Bumps'                 | bool  | Дефект металла: вмятины                          |
| 'Other_Faults'          | bool  | Остальные дефекты                                |
