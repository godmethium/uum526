# -*- coding: utf-8 -*-

class Ui_AnaEkran(object):
    def setupUi(self, AnaEkran, _debug):
        AnaEkran.setObjectName("AnaEkran")
        AnaEkran.resize(870, 280)
        AnaEkran.setMinimumSize(QtCore.QSize(870, 280))
        AnaEkran.setMaximumSize(QtCore.QSize(870, 280))
        font = QtGui.QFont()
        font.setPointSize(12)
        AnaEkran.setFont(font)
        self.centralwidget = QtWidgets.QWidget(AnaEkran)
        self.centralwidget.setObjectName("centralwidget")
        self.t_costFunction = QtWidgets.QTextEdit(self.centralwidget)
        self.t_costFunction.setGeometry(QtCore.QRect(200, 30, 641, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.t_costFunction.setFont(font)
        self.t_costFunction.setObjectName("t_costFunction")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 131, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 121, 41))
        self.label_2.setObjectName("label_2")
        self.combo_constraints = QtWidgets.QComboBox(self.centralwidget)
        self.combo_constraints.setGeometry(QtCore.QRect(130, 120, 61, 31))
        self.combo_constraints.setObjectName("combo_constraints")
        self.combo_constraints.addItem("")
        self.t_constraints = QtWidgets.QTextEdit(self.centralwidget)
        self.t_constraints.setGeometry(QtCore.QRect(200, 120, 451, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.t_constraints.setFont(font)
        self.t_constraints.setObjectName("t_constraints")
        self.b_addToConstraints = QtWidgets.QPushButton(self.centralwidget)
        self.b_addToConstraints.setGeometry(QtCore.QRect(660, 120, 181, 61))
        self.b_addToConstraints.setObjectName("b_addToConstraints")
        self.l_constraints = QtWidgets.QLabel(self.centralwidget)
        self.l_constraints.setGeometry(QtCore.QRect(140, 215, 41, 31))
        self.l_constraints.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.l_constraints.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_constraints.setObjectName("l_constraints")
        self.b_solve = QtWidgets.QPushButton(self.centralwidget)
        self.b_solve.setGeometry(QtCore.QRect(430, 200, 181, 61))
        self.b_solve.setObjectName("b_solve")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 210, 131, 41))
        self.label_3.setObjectName("label_3")
        AnaEkran.setCentralWidget(self.centralwidget)

        self.retranslateUi(AnaEkran)
        self.ekAyarlar(AnaEkran, _debug=_debug)
        QtCore.QMetaObject.connectSlotsByName(AnaEkran)

    def retranslateUi(self, AnaEkran):
        _translate = QtCore.QCoreApplication.translate
        AnaEkran.setWindowTitle(_translate("AnaEkran", "Simplex Algorithm Solver"))
        self.t_costFunction.setHtml(_translate("AnaEkran", ""))
        self.label.setText(_translate("AnaEkran", "Cost Function:"))
        self.label_2.setText(_translate("AnaEkran", "Constraints:"))
        self.combo_constraints.setItemText(0, _translate("AnaEkran", "1"))
        self.t_constraints.setHtml(_translate("AnaEkran", ""))
        self.b_addToConstraints.setText(_translate("AnaEkran", "Add to Constraints"))
        self.l_constraints.setText(_translate("AnaEkran", "0"))
        self.b_solve.setText(_translate("AnaEkran", "Solve"))
        self.label_3.setText(_translate("AnaEkran", "Number of C.:"))

    def ekAyarlar(self, AnaEkran, _debug):
        self.b_addToConstraints.clicked.connect(self.sf_addToConstraints)
        self.b_solve.clicked.connect(self.sf_solve)
        self.combo_constraints.currentTextChanged.connect(self.on_combobox_changed)

        self.cost_function = {}
        self.constraints = []
        self.number_of_constraints = 0
        self.first_opens = False

        self.DEBUG = _debug

    def on_combobox_changed(self):
        try:
            index = self.get_combobox_value()
            # print(index)
            if index <= len(self.constraints):
                _text = ""
                for _name, _value in self.constraints[index-1]["variables"].items():
                    if _value < 0:
                        _text += str(_value) + "*" + _name
                    else:
                        _text += "+" + str(_value) + "*" + _name
                if self.constraints[index-1]["comparison"] == 0b100:
                    _text += "="
                elif self.constraints[index - 1]["comparison"] == 0b101:
                    _text += "<="
                elif self.constraints[index - 1]["comparison"] == 0b110:
                    _text += ">="
                else:
                    pass
                _text += str(self.constraints[index - 1]["RHS"])
                self.t_constraints.setText(_text)
            else:
                self.t_constraints.setText("")
        except Exception as e:
            pass

    def get_equation_parameters(self, option):
        text = ""
        if option == 1:
            text = self.t_costFunction.toPlainText()
            # print(text)

            text = text.replace(" ", "")
            # print(text)

            state = 0b00
            if "min" in text:
                state |= 0b01
            elif "max" in text:
                state |= 0b10
            # print(state)
            text = re.split('min|max', text)
            # print(text)

            rhs = text[1]
            parts = []

            i_p = 0
            i_p_p = 0
            start = False
            for char in rhs:
                if char == "+" or char == "-":
                    if start:
                        parts.append(rhs[i_p_p:i_p])
                        i_p_p = i_p * 1
                    else:
                        start = True
                elif i_p == len(rhs) - 1:
                    if start:
                        parts.append(rhs[i_p_p:i_p + 1])
                        i_p_p = i_p * 1
                    else:
                        start = True
                i_p += 1

            # print(parts)

            variables = {}
            for part in parts:
                part = part.split("*")
                # print(part)
                variables[part[1]] = float(eval(part[0]))
            subject = int(state)
            self.cost_function["variables"] = variables
            self.cost_function["subject"] = subject
            # print(self.cost_function)
        else:
            text = self.t_constraints.toPlainText()
            # print(text)

            text = text.replace(" ", "")
            # print(text)

            state = 0b000
            if "<" in text:
                state |= 0b001
            elif ">" in text:
                state |= 0b010
            if "=" in text:
                state |= 0b100
            # print(state)
            text = re.split('<=|>=|=', text)
            # print(text)

            lhs = text[0]
            rhs = float(eval(text[1]))
            comparison = int(state)
            parts = []

            i_p = 0
            i_p_p = 0
            start = False
            for char in lhs:
                if char == "+" or char == "-":
                    if start:
                        parts.append(lhs[i_p_p:i_p])
                        i_p_p = i_p * 1
                    else:
                        start = True
                elif i_p == len(lhs) - 1:
                    if start:
                        parts.append(lhs[i_p_p:i_p + 1])
                        i_p_p = i_p * 1
                    else:
                        start = True
                i_p += 1

            # print(parts)

            variables = {}
            for part in parts:
                part = part.split("*")
                # print(part)
                variables[part[1]] = float(eval(part[0]))

            # print("Variables:", variables)
            # print("RHS:", rhs)
            # print("Comparison:", comparison)

            dict_ = {}
            dict_["variables"] = variables
            dict_["RHS"] = rhs
            dict_["comparison"] = comparison
            const_index = self.get_combobox_value() - 1
            if const_index < self.number_of_constraints:
                self.constraints[const_index] = dict_
            else:
                self.constraints.append(dict_)
                self.number_of_constraints += 1
                self.l_constraints.setText(str(self.number_of_constraints))
                self.combo_constraints.addItem("")
                self.combo_constraints.setItemText(self.number_of_constraints, str(self.number_of_constraints + 1))
            # print(self.constraints)

    def get_combobox_value(self):
        return int(self.combo_constraints.currentText())

    def sf_addToConstraints(self):
        self.get_equation_parameters(0)

    def sf_add_cost_function(self):
        self.get_equation_parameters(1)

    def sf_convert_to_min_problem(self):
        if self.DEBUG:
            print("---------------Convert to Min Problem--------------------")
        if self.cost_function["subject"] == 1:
            pass
        else:
            if self.DEBUG:
                print("Before ---> ", self.cost_function)
            for var in self.cost_function["variables"]:
                # print(self.cost_function["variables"][var])
                self.cost_function["variables"][var] *= -1
            self.cost_function["subject"] = 1
            if self.DEBUG:
                print("After ----> ",  self.cost_function, "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_make_rhs_positive(self):
        if self.DEBUG:
            print("------------------Make RHS Positive----------------------")
        for i in range(len(self.constraints)):
            if self.constraints[i]["RHS"] < 0:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                for var in self.constraints[i]["variables"]:
                    self.constraints[i]["variables"][var] *= -1
                self.constraints[i]["RHS"] *= -1
                if self.constraints[i]["comparison"] == 4:
                    pass
                else:
                    self.constraints[i]["comparison"] ^= 0b011
                if self.DEBUG:
                    print("After ----> ", self.constraints[i], "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_is_rhs_zero(self):
        if self.DEBUG:
            print("---------------If RHS is Zero and >=---------------------")
        for i in range(len(self.constraints)):
            if self.constraints[i]["RHS"] == 0 and self.constraints[i]["comparison"] == 0b110:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                for var in self.constraints[i]["variables"]:
                    self.constraints[i]["variables"][var] *= -1
                self.constraints[i]["comparison"] = 0b101
                if self.DEBUG:
                    print("After ----> ", self.constraints[i], "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_surplus_variables(self):
        # Comparison is not changed in this function
        if self.DEBUG:
            print("---------------Add Surplus Variables---------------------")
        i_sp = 1
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == 0b110:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding surplus variable...")
                _name = "sp" + str(i_sp)
                self.constraints[i]["variables"][_name] = -1
                i_sp += 1
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_artificial_variables(self):
        if self.DEBUG:
            print("---------------Add Artificial Variables------------------")
        i_a = 1
        self.ai = False
        self.ai_constraints = []
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == 0b110 or self.constraints[i]["comparison"] == 0b100:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding artificial variable...")
                _name = "a" + str(i_a)
                self.constraints[i]["variables"][_name] = 1
                self.constraints[i]["comparison"] = int(0b100)
                i_a += 1
                self.ai = True
                self.ai_constraints.append(i)
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_slack_variables(self):
        if self.DEBUG:
            print("---------------Add Slack Variables-----------------------")
        i_s = 1
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == int(0b101):
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding slack variable...")
                _name = "s" + str(i_s)
                self.constraints[i]["variables"][_name] = 1
                self.constraints[i]["comparison"] = int(0b100)
                i_s += 1
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_artificial_cost_function(self):
        if self.DEBUG:
            print("####################### Add Artificial Cost Function ######################\n")
        if self.ai:
            if self.DEBUG:
                print("********************************************************************")
            # print(self.ai_constraints)
            # print(self.ai)
            self.a_cost_function = {}
            _variables = {}
            _rhs = 0
            for i in self.ai_constraints:
                for var in self.constraints[i]["variables"]:
                    if var[0] is "a":
                        continue
                    if var in _variables:
                        _variables[var] += (self.constraints[i]["variables"][var]) * -1
                    else:
                        _variables[var] = (self.constraints[i]["variables"][var]) * -1
                _rhs += self.constraints[i]["RHS"]
            self.a_cost_function["variables"] = _variables
            self.a_cost_function["RHS"] = _rhs
            self.a_cost_function["comparison"] = 0b100
            if self.DEBUG:
                print("Artificial CF --> \n", self.a_cost_function)
            # print("********************************************************************")
        else:
            pass
        if self.DEBUG:
            print("######################################################################\n")

    def sf_convert_to_lp_problem(self):
        if self.DEBUG:
            print("####################### Convert to Standart LP ######################\n")
        self.sf_convert_to_min_problem()
        self.sf_make_rhs_positive()
        self.sf_is_rhs_zero()
        self.sf_add_surplus_variables()
        self.sf_add_artificial_variables()
        self.sf_add_slack_variables()
        self.sf_add_artificial_cost_function()
        if self.DEBUG:
            print("###################### Converted to Standart LP ######################\n")
            print("Result -->\n")
            print("Cost Function --> ", self.cost_function, "\n")
            if self.ai:
                print("Artificial CF --> ", self.a_cost_function, "\n")
            print("constraints -->\n")
            for con in self.constraints:
                print("--> ", con, "\n")
            print("######################################################################\n")

    def sf_convert_to_tableau(self):
        if self.DEBUG:
            print("####################### Convert to Tableau ######################\n")
        all_x_variables = [int(var[1:]) for var in self.cost_function["variables"]]
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "x":
                    all_x_variables.append(int(var[1:]))
        all_s_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "s" and var[1] != "p":
                    all_s_variables.append(int(var[1:]))
        all_sp_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0:2] == "sp":
                    print(var[2:])
                    all_sp_variables.append(int(var[2:]))
        self.all_a_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "a":
                    self.all_a_variables.append(int(var[1:]))
        # print(all_x_variables)
        # print(all_s_variables)
        # print(all_sp_variables)
        # print(all_a_variables)
        all_x_variables_s = sorted(list(set(all_x_variables)))
        all_s_variables_s = sorted(list(set(all_s_variables)))
        all_sp_variables_s = sorted(list(set(all_sp_variables)))
        all_a_variables_s = sorted(list(set(self.all_a_variables)))
        # print(all_x_variables_s)
        # print(all_s_variables_s)
        # print(all_sp_variables_s)
        # print(all_a_variables_s)
        self.total_n_of_variables = len(all_x_variables_s) + len(all_s_variables_s) + len(all_sp_variables_s) + len(all_a_variables_s)
        self.max_pivot_steps = self.total_n_of_variables**2
        self.tableau = {"rows": [[]], "columns": [["Basic"]]}
        for i in range(len(all_x_variables_s)):
            _name = "x" + str(all_x_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_s_variables_s)):
            _name = "s" + str(all_s_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_sp_variables_s)):
            _name = "sp" + str(all_sp_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_a_variables_s)):
            _name = "a" + str(all_a_variables_s[i])
            self.tableau["columns"][0].append(_name)
        self.tableau["columns"][0].append("b")
        self.tableau["columns"][0].append("Ratio")
        if self.DEBUG:
            print("Tableau Columns Index -->\n", self.tableau["columns"])
        if self.ai:
            self.tableau_matrix = np.zeros((self.number_of_constraints+2, self.total_n_of_variables+3), dtype=float)
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.cost_function["variables"]:
                    self.tableau_matrix[-2][j] = self.cost_function["variables"][self.tableau["columns"][0][j]]
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-2][j] = 0  # indicates f-0

                if self.tableau["columns"][0][j] in self.a_cost_function["variables"]:
                    self.tableau_matrix[-1][j] = self.a_cost_function["variables"][self.tableau["columns"][0][j]]
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-1][j] = self.a_cost_function["RHS"] * -1  # indicates w-rhs
        else:
            self.tableau_matrix = np.zeros((self.number_of_constraints+1, self.total_n_of_variables+3), dtype=float)
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.cost_function["variables"]:
                    self.tableau_matrix[-1][j] = self.cost_function["variables"][self.tableau["columns"][0][j]]
                    # print(self.constraints[i]["variables"][self.tableau["rows"][0][j]])
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-1][j] = 0  # indicates f
        # print(self.number_of_constraints)
        # print(len(self.tableau["rows"][0]))
        # print(total_n_of_variables)
        for i in range(self.number_of_constraints):
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.constraints[i]["variables"]:
                    self.tableau_matrix[i][j] = self.constraints[i]["variables"][self.tableau["columns"][0][j]]
                    # print(self.constraints[i]["variables"][self.tableau["rows"][0][j]])
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[i][j] = self.constraints[i]["RHS"]
        if self.DEBUG:
            print("Tableau Matrix -->\n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_find_basics(self):
        if self.DEBUG:
            print("####################### Find Basics ######################\n")
        if self.ai and not self.ai_solution == 1:
            _transpose = np.transpose(self.tableau_matrix[:-2, :-2])
        else:
            _transpose = np.transpose(self.tableau_matrix[:-1, :-2])
        # print(_transpose)
        _basics = []
        self.basic_variables = {}
        for i in range(1, self.total_n_of_variables + 1):
            _is_basic = False
            _basic_column = 0
            for j in range(_transpose[0].size):
                if _is_basic and _transpose[i][j] != 0:
                    _is_basic = False
                    break
                elif (not _is_basic) and _transpose[i][j] == 1:
                    _is_basic = True
                    _basic_column = j
            if _is_basic:
                _basics.append([i, _basic_column])
        # print(_basics)

        _rows = ["a" for i in range(len(_basics))]
        for i in range(len(_basics)):
            _rows[_basics[i][1]] = self.tableau["columns"][0][_basics[i][0]]
        if self.ai and not self.ai_solution == 1:
            _rows.append("CF")
            _rows.append("ACF")
        else:
            _rows.append("CF")
        self.tableau["rows"][0] = _rows
        if self.DEBUG:
            print("Tableau Rows Index -->\n", self.tableau["rows"])
            print("Tableau Matrix -->\n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_check_cost_function(self):
        if self.DEBUG:
            print("########################Check Cost Function#############################\n")
        self.is_neg_in_cf = False
        self.neg_in_cf = []
        for i in range(self.tableau_matrix[-1].size):
            if self.tableau_matrix[-1][i] < 0:
                self.is_neg_in_cf = True
                self.neg_in_cf.append(i)
        if self.DEBUG:
            print(self.neg_in_cf)
            print(self.is_neg_in_cf)
            print("######################################################################\n")

    def sf_check_rhs(self):
        if self.DEBUG:
            print("############################Check RHS#################################\n")
        self.is_neg_in_rhs = False
        self.neg_in_rhs = []
        for i in range(self.number_of_constraints):
            if self.tableau_matrix[i][-2] < 0:
                self.is_neg_in_rhs = True
                self.neg_in_rhs.append(i)
        if self.DEBUG:
            print(self.neg_in_rhs)
            print(self.is_neg_in_rhs)
            print("######################################################################\n")

    def sf_check_ai_cost_function(self):
        if self.DEBUG:
            print("######################Check Artificial CF#############################\n")
        self.is_neg_in_a_cf = False
        self.neg_in_a_cf = []
        self.is_w_zero = False
        for i in range(1, self.tableau_matrix[-1].size-2):
            if self.tableau_matrix[-1][i] < 0:
                self.is_neg_in_a_cf = True
                self.neg_in_a_cf.append(i)
        if not self.is_neg_in_a_cf:
            if self.tableau_matrix[-1][-2] == 0:
                self.is_w_zero = True
        if self.DEBUG:
            print(self.neg_in_a_cf)
            print(self.is_neg_in_a_cf)
            print(self.is_w_zero)
            print("######################################################################\n")

    def sf_find_pivot_point(self):
        if self.DEBUG:
            print("##################Find Pivot Point###############################\n")
        # _val_min = -1 * np.inf
        # for i in range(1, self.tableau_matrix[-1].size-2):
        self.pivot_column = np.argmin(self.tableau_matrix[-1][1:-2]) + 1
        _ratio = np.inf
        for i in range(self.number_of_constraints):
            if not self.tableau_matrix[i][self.pivot_column] == 0:
                self.tableau_matrix[i][-1] = self.tableau_matrix[i][-2] / self.tableau_matrix[i][self.pivot_column]
                if _ratio > self.tableau_matrix[i][-1] > 0:
                    _ratio = self.tableau_matrix[i][-1]
                    self.pivot_row = i
        if self.DEBUG:
            print("pivot column:", self.pivot_column)
            print("pivot row:", self.pivot_row)
            print("######################################################################\n")

    def sf_do_pivot(self):
        if self.DEBUG:
            print("###################### Do Pivot ###############################\n")
        if self.ai and self.ai_solution == 0:
            _matrix = self.tableau_matrix.copy()
            _p_r = self.pivot_row
            _p_c = self.pivot_column
            _matrix[_p_r] = _matrix[_p_r] / _matrix[_p_r][_p_c]
            for i in range(0, _p_r):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            for i in range(_p_r + 1, self.number_of_constraints + 2):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            # print(_matrix)
            self.tableau_matrix = _matrix.copy()
        else:
            _matrix = self.tableau_matrix.copy()
            _p_r = self.pivot_row
            _p_c = self.pivot_column
            _matrix[_p_r] = _matrix[_p_r] / _matrix[_p_r][_p_c]
            for i in range(0, _p_r):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            for i in range(_p_r+1, self.number_of_constraints+1):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            # print(_matrix)
            self.tableau_matrix = _matrix.copy()
        if self.DEBUG:
            print("######################################################################\n")

    def sf_delete_ai_cost_function(self):
        if self.DEBUG:
            print("######################Delete Artificial Ones################################\n")
            print("Tableau Matrix Before Delete--> \n", self.tableau_matrix)
        self.tableau_matrix = self.tableau_matrix[:-1]
        _transpose = np.transpose(self.tableau_matrix)
        _len_ai = len(list(set(self.all_a_variables)))
        _transpose2 = _transpose[:(-2-_len_ai)]
        _transpose2 = np.append(_transpose2, [_transpose[-2]], axis=0)
        _transpose2 = np.append(_transpose2, [_transpose[-1]], axis=0)
        self.tableau_matrix = np.transpose(_transpose2)
        self.total_n_of_variables -= _len_ai
        if self.DEBUG:
            print("Tableau Matrix After Delete--> \n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_pivot(self):
        print("###########################Pivotting###############################\n")
        self.ai_solution = 0
        self.solution = 0
        if self.ai:
            self.ai_pivot_step = 0
            while self.ai_solution == 0:
                if self.ai_pivot_step > self.max_pivot_steps:
                    self.ai_solution = -2
                    break
                self.ai_pivot_step += 1
                print("Phase 1 Step: ", self.ai_pivot_step)
                self.sf_find_basics()
                self.sf_check_ai_cost_function()
                if not self.is_neg_in_a_cf:
                    if not self.is_w_zero:
                        self.ai_solution = -1
                    else:
                        self.ai_solution = 1
                        self.sf_delete_ai_cost_function()
                else:
                    self.sf_find_pivot_point()
                    self.sf_do_pivot()

        if self.ai_solution == -2:
            return

        if (self.ai and self.ai_solution == 1) or not self.ai:
            self.rcf_pivot_step = 0
            while self.solution == 0:
                if self.rcf_pivot_step > self.max_pivot_steps:
                    self.solution = -2
                    break
                self.rcf_pivot_step += 1
                print("Phase 2 Step: ", self.rcf_pivot_step)
                self.sf_find_basics()
                self.sf_check_cost_function()
                if not self.is_neg_in_cf:
                    self.sf_check_rhs()
                    if self.is_neg_in_rhs:
                        self.solution = -1
                    else:
                        self.solution = 1
                else:
                    self.sf_find_pivot_point()
                    self.sf_do_pivot()
        print("######################################################################\n")

    def sf_show_solution(self):
        print("########################Solution################################\n")
        if self.DEBUG:
            print("ai solution: ", self.ai_solution)
            print("solution: ", self.solution)
        if self.ai_solution == -2:
            print("No solution found in allowed pivot steps in Phase 1. Possible unbounded problem.")
        elif self.solution == -2:
            print("No solution found in allowed pivot steps in Phase 2. Possible unbounded problem.")
        elif self.ai_solution == -1:
            print("No solution found in pivot steps in Phase 1. Possible infeasible problem.")
        elif self.solution == -1:
            print("No solution found in pivot steps in Phase 2. Possible infeasible problem.")
        elif self.solution == 1:
            print("The solution is --> \n")
            # başlıklar
            print("Basic\t", end='')
            for i in range(1, self.tableau_matrix[0].size-2):
                print(self.tableau["columns"][0][i], "\t\t", end='')
            print("b")
            for j in range(0, len(self.tableau["rows"][0])):
                print(self.tableau["rows"][0][j] + "\t", end='')
                for i in range(1, self.tableau_matrix[0].size-1):
                    if j == (len(self.tableau["rows"][0]) - 1) and i == (self.tableau_matrix[0].size - 2):
                        if self.tableau_matrix[j][i] > 0:
                            print("f+%.5f" % self.tableau_matrix[j][i], "\t", end='')
                        elif self.tableau_matrix[j][i] == 0:
                            print("f-%.5f" % self.tableau_matrix[j][i], "\t", end='')
                        else:
                            print("f%.5f" % self.tableau_matrix[j][i], "\t", end='')
                    else:
                        print("%.5f" % self.tableau_matrix[j][i], "\t", end='')
                print("")
        print("\n######################################################################\n")

    def clear_env(self):
        self.cost_function = {}
        self.constraints = []
        self.number_of_constraints = 0
        self.first_opens = False
        self.combo_constraints.clear()
        self.combo_constraints.addItem("")
        self.combo_constraints.setItemText(0, "1")
        self.l_constraints.setText("0")
        self.t_costFunction.setText("")
        self.t_constraints.setText("")

    def sf_solve(self):
        self.sf_add_cost_function()
        self.sf_convert_to_lp_problem()
        self.sf_convert_to_tableau()
        self.sf_pivot()
        self.sf_show_solution()
        self.clear_env()

class Consol_Solver():
    def __init__(self, _debug):
        self.cost_function = {}
        self.constraints = []
        self.number_of_constraints = 0
        self.first_opens = False
        self.equations = None
        self.DEBUG = _debug

    def sf_get_equation_parameters(self):
        _e_i = 0
        for line in self.equations.splitlines():
            if _e_i == 0:
                text = line
                text = text.replace(" ", "")
                state = 0b00
                if "min" in text:
                    state |= 0b01
                elif "max" in text:
                    state |= 0b10
                text = re.split('min|max', text)
                rhs = text[1]
                parts = []
                i_p = 0
                i_p_p = 0
                start = False
                for char in rhs:
                    if char == "+" or char == "-":
                        if start:
                            parts.append(rhs[i_p_p:i_p])
                            i_p_p = i_p * 1
                        else:
                            start = True
                    elif i_p == len(rhs) - 1:
                        if start:
                            parts.append(rhs[i_p_p:i_p + 1])
                            i_p_p = i_p * 1
                        else:
                            start = True
                    i_p += 1
                variables = {}
                for part in parts:
                    part = part.split("*")
                    variables[part[1]] = float(eval(part[0]))
                subject = int(state)
                self.cost_function["variables"] = variables
                self.cost_function["subject"] = subject
                _e_i = 1
            else:
                text = line
                text = text.replace(" ", "")
                state = 0b000
                if "<" in text:
                    state |= 0b001
                elif ">" in text:
                    state |= 0b010
                if "=" in text:
                    state |= 0b100
                text = re.split('<=|>=|=', text)
                lhs = text[0]
                rhs = float(eval(text[1]))
                comparison = int(state)
                parts = []
                i_p = 0
                i_p_p = 0
                start = False
                for char in lhs:
                    if char == "+" or char == "-":
                        if start:
                            parts.append(lhs[i_p_p:i_p])
                            i_p_p = i_p * 1
                        else:
                            start = True
                    elif i_p == len(lhs) - 1:
                        if start:
                            parts.append(lhs[i_p_p:i_p + 1])
                            i_p_p = i_p * 1
                        else:
                            start = True
                    i_p += 1
                variables = {}
                for part in parts:
                    part = part.split("*")
                    # print(part)
                    variables[part[1]] = float(eval(part[0]))
                dict_ = {}
                dict_["variables"] = variables
                dict_["RHS"] = rhs
                dict_["comparison"] = comparison
                self.constraints.append(dict_)
                self.number_of_constraints += 1

    def sf_convert_to_min_problem(self):
        if self.DEBUG:
            print("---------------Convert to Min Problem--------------------")
        if self.cost_function["subject"] == 1:
            pass
        else:
            if self.DEBUG:
                print("Before ---> ", self.cost_function)
            for var in self.cost_function["variables"]:
                # print(self.cost_function["variables"][var])
                self.cost_function["variables"][var] *= -1
            self.cost_function["subject"] = 1
            if self.DEBUG:
                print("After ----> ",  self.cost_function, "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_make_rhs_positive(self):
        if self.DEBUG:
            print("------------------Make RHS Positive----------------------")
        for i in range(len(self.constraints)):
            if self.constraints[i]["RHS"] < 0:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                for var in self.constraints[i]["variables"]:
                    self.constraints[i]["variables"][var] *= -1
                self.constraints[i]["RHS"] *= -1
                if self.constraints[i]["comparison"] == 4:
                    pass
                else:
                    self.constraints[i]["comparison"] ^= 0b011
                if self.DEBUG:
                    print("After ----> ", self.constraints[i], "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_is_rhs_zero(self):
        if self.DEBUG:
            print("---------------If RHS is Zero and >=---------------------")
        for i in range(len(self.constraints)):
            if self.constraints[i]["RHS"] == 0 and self.constraints[i]["comparison"] == 0b110:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                for var in self.constraints[i]["variables"]:
                    self.constraints[i]["variables"][var] *= -1
                self.constraints[i]["comparison"] = 0b101
                if self.DEBUG:
                    print("After ----> ", self.constraints[i], "\n")
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_surplus_variables(self):
        # Comparison is not changed in this function
        if self.DEBUG:
            print("---------------Add Surplus Variables---------------------")
        i_sp = 1
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == 0b110:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding surplus variable...")
                _name = "sp" + str(i_sp)
                self.constraints[i]["variables"][_name] = -1
                i_sp += 1
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_artificial_variables(self):
        if self.DEBUG:
            print("---------------Add Artificial Variables------------------")
        i_a = 1
        self.ai = False
        self.ai_constraints = []
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == 0b110 or self.constraints[i]["comparison"] == 0b100:
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding artificial variable...")
                _name = "a" + str(i_a)
                self.constraints[i]["variables"][_name] = 1
                self.constraints[i]["comparison"] = int(0b100)
                i_a += 1
                self.ai = True
                self.ai_constraints.append(i)
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_slack_variables(self):
        if self.DEBUG:
            print("---------------Add Slack Variables-----------------------")
        i_s = 1
        for i in range(len(self.constraints)):
            if self.constraints[i]["comparison"] == int(0b101):
                if self.DEBUG:
                    print("Before ---> ", self.constraints[i])
                    print("adding slack variable...")
                _name = "s" + str(i_s)
                self.constraints[i]["variables"][_name] = 1
                self.constraints[i]["comparison"] = int(0b100)
                i_s += 1
                if self.DEBUG:
                    print("After ----> ",  self.constraints[i])
        if self.DEBUG:
            print("---------------------------------------------------------")

    def sf_add_artificial_cost_function(self):
        if self.DEBUG:
            print("####################### Add Artificial Cost Function ######################\n")
        if self.ai:
            if self.DEBUG:
                print("********************************************************************")
            # print(self.ai_constraints)
            # print(self.ai)
            self.a_cost_function = {}
            _variables = {}
            _rhs = 0
            for i in self.ai_constraints:
                for var in self.constraints[i]["variables"]:
                    if var[0] is "a":
                        continue
                    if var in _variables:
                        _variables[var] += (self.constraints[i]["variables"][var]) * -1
                    else:
                        _variables[var] = (self.constraints[i]["variables"][var]) * -1
                _rhs += self.constraints[i]["RHS"]
            self.a_cost_function["variables"] = _variables
            self.a_cost_function["RHS"] = _rhs
            self.a_cost_function["comparison"] = 0b100
            if self.DEBUG:
                print("Artificial CF --> \n", self.a_cost_function)
            # print("********************************************************************")
        else:
            pass
        if self.DEBUG:
            print("######################################################################\n")

    def sf_convert_to_lp_problem(self):
        if self.DEBUG:
            print("####################### Convert to Standart LP ######################\n")
        self.sf_convert_to_min_problem()
        self.sf_make_rhs_positive()
        self.sf_is_rhs_zero()
        self.sf_add_surplus_variables()
        self.sf_add_artificial_variables()
        self.sf_add_slack_variables()
        self.sf_add_artificial_cost_function()
        if self.DEBUG:
            print("###################### Converted to Standart LP ######################\n")
            print("Result -->\n")
            print("Cost Function --> ", self.cost_function, "\n")
            if self.ai:
                print("Artificial CF --> ", self.a_cost_function, "\n")
            print("constraints -->\n")
            for con in self.constraints:
                print("--> ", con, "\n")
            print("######################################################################\n")

    def sf_convert_to_tableau(self):
        if self.DEBUG:
            print("####################### Convert to Tableau ######################\n")
        all_x_variables = [int(var[1:]) for var in self.cost_function["variables"]]
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "x":
                    all_x_variables.append(int(var[1:]))
        all_s_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "s" and var[1] != "p":
                    all_s_variables.append(int(var[1:]))
        all_sp_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0:2] == "sp":
                    print(var[2:])
                    all_sp_variables.append(int(var[2:]))
        self.all_a_variables = []
        for con in self.constraints:
            for var in con["variables"]:
                if var[0] == "a":
                    self.all_a_variables.append(int(var[1:]))
        # print(all_x_variables)
        # print(all_s_variables)
        # print(all_sp_variables)
        # print(all_a_variables)
        all_x_variables_s = sorted(list(set(all_x_variables)))
        all_s_variables_s = sorted(list(set(all_s_variables)))
        all_sp_variables_s = sorted(list(set(all_sp_variables)))
        all_a_variables_s = sorted(list(set(self.all_a_variables)))
        # print(all_x_variables_s)
        # print(all_s_variables_s)
        # print(all_sp_variables_s)
        # print(all_a_variables_s)
        self.total_n_of_variables = len(all_x_variables_s) + len(all_s_variables_s) + len(all_sp_variables_s) + len(all_a_variables_s)
        self.max_pivot_steps = self.total_n_of_variables**2
        self.tableau = {"rows": [[]], "columns": [["Basic"]]}
        for i in range(len(all_x_variables_s)):
            _name = "x" + str(all_x_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_s_variables_s)):
            _name = "s" + str(all_s_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_sp_variables_s)):
            _name = "sp" + str(all_sp_variables_s[i])
            self.tableau["columns"][0].append(_name)
        for i in range(len(all_a_variables_s)):
            _name = "a" + str(all_a_variables_s[i])
            self.tableau["columns"][0].append(_name)
        self.tableau["columns"][0].append("b")
        self.tableau["columns"][0].append("Ratio")
        if self.DEBUG:
            print("Tableau Columns Index -->\n", self.tableau["columns"])
        if self.ai:
            self.tableau_matrix = np.zeros((self.number_of_constraints+2, self.total_n_of_variables+3), dtype=float)
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.cost_function["variables"]:
                    self.tableau_matrix[-2][j] = self.cost_function["variables"][self.tableau["columns"][0][j]]
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-2][j] = 0  # indicates f-0

                if self.tableau["columns"][0][j] in self.a_cost_function["variables"]:
                    self.tableau_matrix[-1][j] = self.a_cost_function["variables"][self.tableau["columns"][0][j]]
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-1][j] = self.a_cost_function["RHS"] * -1  # indicates w-rhs
        else:
            self.tableau_matrix = np.zeros((self.number_of_constraints+1, self.total_n_of_variables+3), dtype=float)
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.cost_function["variables"]:
                    self.tableau_matrix[-1][j] = self.cost_function["variables"][self.tableau["columns"][0][j]]
                    # print(self.constraints[i]["variables"][self.tableau["rows"][0][j]])
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[-1][j] = 0  # indicates f
        # print(self.number_of_constraints)
        # print(len(self.tableau["rows"][0]))
        # print(total_n_of_variables)
        for i in range(self.number_of_constraints):
            for j in range(len(self.tableau["columns"][0])):
                if self.tableau["columns"][0][j] in self.constraints[i]["variables"]:
                    self.tableau_matrix[i][j] = self.constraints[i]["variables"][self.tableau["columns"][0][j]]
                    # print(self.constraints[i]["variables"][self.tableau["rows"][0][j]])
                elif self.tableau["columns"][0][j] == "b":
                    self.tableau_matrix[i][j] = self.constraints[i]["RHS"]
        if self.DEBUG:
            print("Tableau Matrix -->\n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_find_basics(self):
        if self.DEBUG:
            print("####################### Find Basics ######################\n")
        if self.ai and not self.ai_solution == 1:
            _transpose = np.transpose(self.tableau_matrix[:-2, :-2])
        else:
            _transpose = np.transpose(self.tableau_matrix[:-1, :-2])
        # print(_transpose)
        _basics = []
        self.basic_variables = {}
        for i in range(1, self.total_n_of_variables + 1):
            _is_basic = False
            _basic_column = 0
            for j in range(_transpose[0].size):
                if _is_basic and _transpose[i][j] != 0:
                    _is_basic = False
                    break
                elif (not _is_basic) and _transpose[i][j] == 1:
                    _is_basic = True
                    _basic_column = j
            if _is_basic:
                _basics.append([i, _basic_column])
        # print(_basics)

        _rows = ["a" for i in range(len(_basics))]
        for i in range(len(_basics)):
            _rows[_basics[i][1]] = self.tableau["columns"][0][_basics[i][0]]
        if self.ai and not self.ai_solution == 1:
            _rows.append("CF")
            _rows.append("ACF")
        else:
            _rows.append("CF")
        self.tableau["rows"][0] = _rows
        if self.DEBUG:
            print("Tableau Rows Index -->\n", self.tableau["rows"])
            print("Tableau Matrix -->\n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_check_cost_function(self):
        if self.DEBUG:
            print("########################Check Cost Function#############################\n")
        self.is_neg_in_cf = False
        self.neg_in_cf = []
        for i in range(self.tableau_matrix[-1].size):
            if self.tableau_matrix[-1][i] < 0:
                self.is_neg_in_cf = True
                self.neg_in_cf.append(i)
        if self.DEBUG:
            print(self.neg_in_cf)
            print(self.is_neg_in_cf)
            print("######################################################################\n")

    def sf_check_rhs(self):
        if self.DEBUG:
            print("############################Check RHS#################################\n")
        self.is_neg_in_rhs = False
        self.neg_in_rhs = []
        for i in range(self.number_of_constraints):
            if self.tableau_matrix[i][-2] < 0:
                self.is_neg_in_rhs = True
                self.neg_in_rhs.append(i)
        if self.DEBUG:
            print(self.neg_in_rhs)
            print(self.is_neg_in_rhs)
            print("######################################################################\n")

    def sf_check_ai_cost_function(self):
        if self.DEBUG:
            print("######################Check Artificial CF#############################\n")
        self.is_neg_in_a_cf = False
        self.neg_in_a_cf = []
        self.is_w_zero = False
        for i in range(1, self.tableau_matrix[-1].size-2):
            if self.tableau_matrix[-1][i] < 0:
                self.is_neg_in_a_cf = True
                self.neg_in_a_cf.append(i)
        if not self.is_neg_in_a_cf:
            if self.tableau_matrix[-1][-2] == 0:
                self.is_w_zero = True
        if self.DEBUG:
            print(self.neg_in_a_cf)
            print(self.is_neg_in_a_cf)
            print(self.is_w_zero)
            print("######################################################################\n")

    def sf_find_pivot_point(self):
        if self.DEBUG:
            print("##################Find Pivot Point###############################\n")
        # _val_min = -1 * np.inf
        # for i in range(1, self.tableau_matrix[-1].size-2):
        self.pivot_column = np.argmin(self.tableau_matrix[-1][1:-2]) + 1
        _ratio = np.inf
        for i in range(self.number_of_constraints):
            if not self.tableau_matrix[i][self.pivot_column] == 0:
                self.tableau_matrix[i][-1] = self.tableau_matrix[i][-2] / self.tableau_matrix[i][self.pivot_column]
                if _ratio > self.tableau_matrix[i][-1] > 0:
                    _ratio = self.tableau_matrix[i][-1]
                    self.pivot_row = i
        if self.DEBUG:
            print("pivot column:", self.pivot_column)
            print("pivot row:", self.pivot_row)
            print("######################################################################\n")

    def sf_do_pivot(self):
        if self.DEBUG:
            print("###################### Do Pivot ###############################\n")
        if self.ai and self.ai_solution == 0:
            _matrix = self.tableau_matrix.copy()
            _p_r = self.pivot_row
            _p_c = self.pivot_column
            _matrix[_p_r] = _matrix[_p_r] / _matrix[_p_r][_p_c]
            for i in range(0, _p_r):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            for i in range(_p_r + 1, self.number_of_constraints + 2):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            # print(_matrix)
            self.tableau_matrix = _matrix.copy()
        else:
            _matrix = self.tableau_matrix.copy()
            _p_r = self.pivot_row
            _p_c = self.pivot_column
            _matrix[_p_r] = _matrix[_p_r] / _matrix[_p_r][_p_c]
            for i in range(0, _p_r):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            for i in range(_p_r+1, self.number_of_constraints+1):
                _matrix_ = (_matrix[i][_p_c] / _matrix[_p_r][_p_c]) * _matrix[_p_r]
                _matrix[i] = _matrix[i] - _matrix_
            # print(_matrix)
            self.tableau_matrix = _matrix.copy()
        if self.DEBUG:
            print("######################################################################\n")

    def sf_delete_ai_cost_function(self):
        if self.DEBUG:
            print("######################Delete Artificial Ones################################\n")
            print("Tableau Matrix Before Delete--> \n", self.tableau_matrix)
        self.tableau_matrix = self.tableau_matrix[:-1]
        _transpose = np.transpose(self.tableau_matrix)
        _len_ai = len(list(set(self.all_a_variables)))
        _transpose2 = _transpose[:(-2-_len_ai)]
        _transpose2 = np.append(_transpose2, [_transpose[-2]], axis=0)
        _transpose2 = np.append(_transpose2, [_transpose[-1]], axis=0)
        self.tableau_matrix = np.transpose(_transpose2)
        self.total_n_of_variables -= _len_ai
        if self.DEBUG:
            print("Tableau Matrix After Delete--> \n", self.tableau_matrix)
            print("######################################################################\n")

    def sf_pivot(self):
        print("###########################Pivotting###############################\n")
        self.ai_solution = 0
        self.solution = 0
        if self.ai:
            self.ai_pivot_step = 0
            while self.ai_solution == 0:
                if self.ai_pivot_step > self.max_pivot_steps:
                    self.ai_solution = -2
                    break
                self.ai_pivot_step += 1
                print("Phase 1 Step: ", self.ai_pivot_step)
                self.sf_find_basics()
                self.sf_check_ai_cost_function()
                if not self.is_neg_in_a_cf:
                    if not self.is_w_zero:
                        self.ai_solution = -1
                    else:
                        self.ai_solution = 1
                        self.sf_delete_ai_cost_function()
                else:
                    self.sf_find_pivot_point()
                    self.sf_do_pivot()

        if self.ai_solution == -2:
            return

        if (self.ai and self.ai_solution == 1) or not self.ai:
            self.rcf_pivot_step = 0
            while self.solution == 0:
                if self.rcf_pivot_step > self.max_pivot_steps:
                    self.solution = -2
                    break
                self.rcf_pivot_step += 1
                print("Phase 2 Step: ", self.rcf_pivot_step)
                self.sf_find_basics()
                self.sf_check_cost_function()
                if not self.is_neg_in_cf:
                    self.sf_check_rhs()
                    if self.is_neg_in_rhs:
                        self.solution = -1
                    else:
                        self.solution = 1
                else:
                    self.sf_find_pivot_point()
                    self.sf_do_pivot()
        print("######################################################################\n")

    def sf_show_solution(self):
        print("########################Solution################################\n")
        if self.DEBUG:
            print("ai solution: ", self.ai_solution)
            print("solution: ", self.solution)
        if self.ai_solution == -2:
            print("No solution found in allowed pivot steps in Phase 1. Possible unbounded problem.")
        elif self.solution == -2:
            print("No solution found in allowed pivot steps in Phase 2. Possible unbounded problem.")
        elif self.ai_solution == -1:
            print("No solution found in pivot steps in Phase 1. Possible infeasible problem.")
        elif self.solution == -1:
            print("No solution found in pivot steps in Phase 2. Possible infeasible problem.")
        elif self.solution == 1:
            print("The solution is --> \n")
            # başlıklar
            print("Basic\t", end='')
            for i in range(1, self.tableau_matrix[0].size-2):
                print(self.tableau["columns"][0][i], "\t\t", end='')
            print("b")
            for j in range(0, len(self.tableau["rows"][0])):
                print(self.tableau["rows"][0][j] + "\t", end='')
                for i in range(1, self.tableau_matrix[0].size-1):
                    if j == (len(self.tableau["rows"][0]) - 1) and i == (self.tableau_matrix[0].size - 2):
                        if self.tableau_matrix[j][i] > 0:
                            print("f+%.5f" % self.tableau_matrix[j][i], "\t", end='')
                        elif self.tableau_matrix[j][i] == 0:
                            print("f-%.5f" % self.tableau_matrix[j][i], "\t", end='')
                        else:
                            print("f%.5f" % self.tableau_matrix[j][i], "\t", end='')
                    else:
                        print("%.5f" % self.tableau_matrix[j][i], "\t", end='')
                print("")
        print("\n######################################################################\n")

    def clear_env(self):
        self.cost_function = {}
        self.constraints = []
        self.number_of_constraints = 0
        self.first_opens = False
        self.equations = None

    def sf_solve(self):
        self.sf_get_equation_parameters()
        self.sf_convert_to_lp_problem()
        self.sf_convert_to_tableau()
        self.sf_pivot()
        self.sf_show_solution()
        self.clear_env()

    def Solve(self, _equations):
        self.equations = _equations
        self.sf_solve()

if __name__ == "__main__":
    import argparse
    import sys
    import re
    import numpy as np

    np.set_printoptions(threshold=sys.maxsize)

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Open GUI", action="store_true")
    parser.add_argument("-c", help="Solves the problem given in the desired format in the .txt file.",
                        action="store_true")
    parser.add_argument("-i", required=False, help="Specifies the .txt file containing the problem.")
    parser.add_argument("-d", required=False, help="Enters debug mode.", action="store_true")
    args = parser.parse_args()
    args_vars = vars(parser.parse_args())
    _debug = False
    if args.d:
        _debug = True
    if args.g:
        from PyQt5 import QtCore, QtGui, QtWidgets
        app = QtWidgets.QApplication(sys.argv)
        AnaEkran = QtWidgets.QMainWindow()
        ui = Ui_AnaEkran()
        ui.setupUi(AnaEkran, _debug=_debug)
        AnaEkran.show()
        sys.exit(app.exec_())
    elif args.c:
        if args_vars["i"] is not None:
            # _equations = "max +1*x1+2*x2-2*x3\n+3*x1+2*x2-2*x3<=12\n+2*x1+3*x2-3*x3>=6"
            _equations = (open(args_vars["i"], "r").read())
            Simplex = Consol_Solver(_debug=_debug)
            Simplex.Solve(_equations=_equations)
        else:
            print("Please specify the .txt file path.")
            print("e.g. --> python simplex.py -c -i problem.txt")
