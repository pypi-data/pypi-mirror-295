# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 12:59:08 2024

@author: BernardoCastro
"""
import numpy as np
from prettytable import PrettyTable as pt
import matplotlib.pyplot as plt
import pandas as pd

class Results:
    def __init__(self, Grid, decimals=2, export=False):
        self.Grid = Grid
        self.dec = decimals
        self.export = export

    def options(self):
        # Create an instance of the class
        my_instance = self

        # Get all attributes (including methods) of the class
        all_attributes = dir(self)

        # Filter out only the methods (defs)
        methods = [attribute for attribute in all_attributes if callable(
            getattr(self, attribute)) and not attribute.startswith('__')]

        # Print the method names
        for method_name in methods:
            print(method_name)
    # def export(self):

    def All(self):

        self.AC_Powerflow()
        self.AC_voltage()
        self.AC_lines_current()
        self.AC_lines_power()
        
        if self.Grid.nodes_DC != None:
            if self.Grid.nconv != 0:
                self.Converter()
            self.DC_bus()
            self.DC_lines_current()
            self.DC_lines_power()
            self.Slack_All()
        else:
            self.Slack_AC()

        self.Power_loss()
        if self.Grid.OPF_run == True:
            self.Ext_gen()
            if any(node.extGrid == 3 for node in self.Grid.nodes_AC):
            
                self.Ext_WPP()
            self.Market()    
        print('------')

    def All_AC(self):
        self.AC_Powerflow()
        self.AC_voltage()
        self.AC_lines_current()
        self.AC_lines_power()
        self.Slack_AC()
        self.Power_loss_AC()

    def All_DC(self):

        if self.Grid.nconv != 0:
            self.Converter()

        self.DC_bus()

        self.DC_lines_current()
        self.DC_lines_power()
        self.Slack_DC()
        self.Power_loss_DC()

        if self.Grid.Converters_DCDC != None:
            self.DC_converter()

    def Slack_All(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Slack node"]

        for i in range(self.Grid.Num_Grids_AC):
            for node in self.Grid.Grids_AC[i]:
                if node.type == 'Slack':
                    table.add_row([f'AC Grid {i+1}', node.name])
        for i in range(self.Grid.Num_Grids_DC):
            for node in self.Grid.Grids_DC[i]:
                if node.type == 'Slack':
                    table.add_row([f'DC Grid {i+1}', node.name])

        print('--------------')
        print(f'Slack nodes')
        print(table)

    def Slack_AC(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Slack node"]

        for i in range(self.Grid.Num_Grids_AC):
            for node in self.Grid.Grids_AC[i]:
                if node.type == 'Slack':
                    table.add_row([f'AC Grid {i+1}', node.name])

        print('--------------')
        print(f'Slack nodes')
        print(table)

    def Slack_DC(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Slack node"]
        slack = 0
        for i in range(self.Grid.Num_Grids_DC):
            for node in self.Grid.Grids_DC[i]:
                if node.type == 'Slack':
                    table.add_row([f'DC Grid {i+1}', node.name])
                    slack += 1

        print('--------------')
        print(f'Slack nodes')
        if slack == 0:
            print("No DC nodes are set as Slack")
        else:
            print(table)

    def DC_converter(self):
        table = pt()

        table.field_names = ["Converter", "From node", "To node",
                             "Power from (MW)", "Power To (MW))", "Power Loss (MW)"]
        for conv in self.Grid.Converters_DCDC:
            convid = conv.name
            fromnode = conv.fromNode.name
            tonode = conv.toNode.name
            fromMW = conv.Powerfrom*self.Grid.S_base
            toMW = conv.PowerTo*self.Grid.S_base
            loss = fromMW-toMW

            table.add_row([convid, fromnode, tonode, np.round(fromMW, decimals=self.dec), np.round(
                toMW, decimals=self.dec), np.round(loss, decimals=self.dec)])
        print('-----------')
        print('DC DC Coverters')
        print(table)

    def Power_loss(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Power Loss (MW)","Load %"]
        if self.Grid.nodes_AC != None:
            self.lossP_AC = np.zeros(self.Grid.Num_Grids_AC)
            for line in self.Grid.lines_AC:
                node = line.fromNode
                G = self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber]
                Ploss = np.real(line.loss)*self.Grid.S_base
                Qloss = np.imag(line.loss)*self.Grid.S_base
                
                     
                i = line.fromNode.nodeNumber
                j = line.toNode.nodeNumber
                Sfrom = abs(self.Grid.Sij[i, j]*self.Grid.S_base)
                Sto = abs(self.Grid.Sij[j, i]*self.Grid.S_base)

                load = max(Sfrom, Sto)
                
                self.Grid.load_grid_AC[G] += load
                
                self.lossP_AC[G] += Ploss
                
            tot = 0
            for g in range(self.Grid.Num_Grids_AC):
                if self.Grid.rating_grid_AC[g]!=0:
                    gload=self.Grid.load_grid_AC[g]/self.Grid.rating_grid_AC[g]*100
                else:
                    gload=0
                table.add_row([f'AC Grid {g+1}', np.round(self.lossP_AC[g], decimals=self.dec),np.round(gload, decimals=self.dec)])
                tot += self.lossP_AC[g]

        if self.Grid.nodes_DC != None:

            self.lossP_DC = np.zeros(self.Grid.Num_Grids_DC)

            for line in self.Grid.lines_DC:
                node = line.fromNode
                G = self.Grid.Graph_node_to_Grid_index_DC[node.nodeNumber]

                Ploss = np.real(line.loss)*self.Grid.S_base
                
                self.lossP_DC[G] += Ploss
                
                       
                i = line.fromNode.nodeNumber
                j = line.toNode.nodeNumber
                p_to = self.Grid.Pij_DC[j, i]*self.Grid.S_base
                p_from = self.Grid.Pij_DC[i, j]*self.Grid.S_base

                load = max(p_to, p_from)
                
                self.Grid.load_grid_DC[G] += load
                
                
            for g in range(self.Grid.Num_Grids_DC):
                gload=self.Grid.load_grid_DC[g]/self.Grid.rating_grid_DC[g]*100
                table.add_row([f'DC Grid {g+1}', np.round(self.lossP_DC[g], decimals=self.dec),np.round(gload, decimals=self.dec)])
                tot += self.lossP_DC[g]

        if self.Grid.Converters_ACDC != None:
            P_loss_ACDC = 0
            for conv in self.Grid.Converters_ACDC:
                P_loss_ACDC += (conv.P_loss_tf+conv.P_loss)*self.Grid.S_base
                tot += (conv.P_loss_tf+conv.P_loss)*self.Grid.S_base
                s = 1

            table.add_row([f'AC DC Converters', np.round(P_loss_ACDC, decimals=self.dec),""])

        if self.Grid.Converters_DCDC != None:
            P_loss_DCDC = 0
            for conv in self.Grid.Converters_DCDC:
                P_loss_DCDC += (abs(conv.PowerTo-conv.Powerfrom))*self.Grid.S_base
                tot += (abs(conv.PowerTo-conv.Powerfrom))*self.Grid.S_base

            table.add_row([f'DC DC Converters', np.round(P_loss_DCDC, decimals=self.dec),""])

        table.add_row(["Total loss", np.round(tot, decimals=self.dec),""])
        print('--------------')
        print(f'Power loss')
        print(table)

    def Power_loss_AC(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Power Loss (MW)"]
        self.lossP_AC = np.zeros(self.Grid.Num_Grids_AC)
        for line in self.Grid.lines_AC:
            node = line.fromNode
            G = self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber]
            Ploss = np.real(line.loss)*self.Grid.S_base
            Qloss = np.imag(line.loss)*self.Grid.S_base

            self.lossP_AC[G] += Ploss

        tot = 0
        for g in range(self.Grid.Num_Grids_AC):
            table.add_row(
                [f'AC Grid {g+1}', np.round(self.lossP_AC[g], decimals=self.dec)])
            tot += self.lossP_AC[g]

        table.add_row(["Total loss", np.round(tot, decimals=self.dec)])
        print('--------------')
        print(f'Power loss AC')
        print(table)

    def Power_loss_DC(self):
        table = pt()
        # Define the table headers
        table.field_names = ["Grid", "Power Loss (MW)"]

        self.lossP_DC = np.zeros(self.Grid.Num_Grids_DC)

        for line in self.Grid.lines_DC:
            node = line.fromNode
            G = self.Grid.Graph_node_to_Grid_index_DC[node]

            Ploss = np.real(line.loss)*self.Grid.S_base

            self.lossP_DC[G] += Ploss
        tot = 0

        for g in range(self.Grid.Num_Grids_DC):
            table.add_row(
                [f'DC Grid {g+1}', np.round(self.lossP_DC[g], decimals=self.dec)])
            tot += self.lossP_DC[g]

        table.add_row(["Total loss", np.round(tot, decimals=self.dec)])
        print('--------------')
        print(f'Power loss DC')
        print(table)

    def DC_bus(self):
        print('--------------')
        print(f'Results DC')
        print('')
        table_all = pt()
        table_all.field_names = [
            "Node", "Power Gen (MW)", "Power Load (MW)", "Power Converter ACDC (MW)", "Power Converter DCDC (MW)", "Power injected (MW)", "Voltage (pu)", "Grid"]
        for g in range(self.Grid.Num_Grids_DC):
            print(f'Grid DC {g+1}')

            table = pt()

            # Define the table headers
            table.field_names = [
                "Node", "Power Gen (MW)", "Power Load (MW)", "Power Converter ACDC (MW)", "Power Converter DCDC (MW)", "Power injected (MW)", "Voltage (pu)"]

            for node in self.Grid.nodes_DC:
                if self.Grid.Graph_node_to_Grid_index_DC[node.nodeNumber] == g:
                    if node.type == 'Slack':
                        if self.Grid.nconv == 0:
                            if node.P_INJ > 0:
                                node.PGi = node.P_INJ
                            else:
                                node.PLi = abs(node.P_INJ)
                    conv  = np.round(node.P*self.Grid.S_base, decimals=self.dec)
                    convDC =np.round(node.PconvDC *self.Grid.S_base, decimals=self.dec)
                    table.add_row([node.name, np.round(node.PGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base,
                                  decimals=self.dec), conv,convDC, np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.V, decimals=self.dec)])
                    table_all.add_row([node.name, np.round(node.PGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base,
                                      decimals=self.dec), conv,convDC, np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.V, decimals=self.dec), g+1])

            print(table)

        if self.export == True:
            csv_filename = 'DC_bus.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def AC_Powerflow(self, Grid=None):
        print('--------------')
        print(f'Results AC power')
        print('')
        table_all = pt()

        if self.Grid.nodes_DC == None:
            table_all.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)",
                                     "Reactive Load (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)", "Grid"]
        else:
            table_all.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)", "Reactive Load (MVAR)",
                                     "Power converters DC(MW)", "Reactive converters DC (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)", "Grid"]

        for g in range(self.Grid.Num_Grids_AC):
            if Grid == (g+1):
                print(f'Grid AC {g+1}')
                table = pt()
                if self.Grid.nodes_DC == None:
                    # Define the table headers
                    table.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)",
                                         "Reactive Load (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)"]

                    for node in self.Grid.nodes_AC:
                        if self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber] == g:
                            PGi = node.PGi+node.PGi_ren*node.curtailment +node.PGi_opt
                            QGi = node.QGi +node.QGi_opt
                            if node.type == 'Slack':
                                PGi = node.P_INJ+node.PLi
                                QGi = node.Q_INJ+node.QLi

                            if node.type == 'PV':
                                node.QGi = node.Q_INJ - \
                                    (node.Q_s+node.Q_s_fx)+node.QLi

                            table.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.QLi*self.Grid.S_base, decimals=self.dec), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec)])

                else:
                    # Define the table headers
                    table.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)", "Reactive Load (MVAR)",
                                         "Power converters DC(MW)", "Reactive converters DC (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)"]

                    for node in self.Grid.nodes_AC:
                        if self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber] == g:
                            PGi = node.PGi +node.PGi_res*node.curtailment+node.PGi_opt
                            QGi = node.QGi +node.QGi_opt
                            if node.type == 'Slack':
                                PGi = (node.P_INJ-node.P_s + node.PLi).item()
                                QGi = node.Q_INJ-node.Q_s-node.Q_s_fx+node.QLi

                            if node.type == 'PV':
                                QGi = node.Q_INJ -(node.Q_s+node.Q_s_fx)+node.QLi

                            table.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(node.QLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.P_s*self.Grid.S_base, decimals=self.dec).item(), np.round((node.Q_s+node.Q_s_fx)*self.Grid.S_base, decimals=self.dec).item(), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec)])
                            s = 1
                print(table)

            elif Grid == None:
                print(f'Grid AC {g+1}')
                table = pt()
                if self.Grid.nodes_DC == None:
                    # Define the table headers
                    table.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)",
                                         "Reactive Load (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)"]

                    for node in self.Grid.nodes_AC:
                        if self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber] == g:
                            PGi = node.PGi+node.PGi_ren*node.curtailment +node.PGi_opt
                            QGi = node.QGi +node.QGi_opt
                            if node.type == 'Slack':
                                PGi = node.P_INJ+node.PLi
                                QGi = node.Q_INJ+node.QLi

                            if node.type == 'PV':
                                node.QGi = node.Q_INJ - \
                                    (node.Q_s+node.Q_s_fx)+node.QLi

                            table.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.QLi*self.Grid.S_base, decimals=self.dec), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec)])
                            table_all.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.QLi*self.Grid.S_base, decimals=self.dec), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec), g+1])

                else:
                    # Define the table headers
                    table.field_names = ["Node", "Power Gen (MW)", "Reactive Gen (MVAR)", "Power Load (MW)", "Reactive Load (MVAR)",
                                         "Power converters DC(MW)", "Reactive converters DC (MVAR)", "Power injected  (MW)", "Reactive injected  (MVAR)"]

                    for node in self.Grid.nodes_AC:
                        if self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber] == g:
                            PGi = node.PGi+node.PGi_ren*node.curtailment +node.PGi_opt
                            QGi = node.QGi +node.QGi_opt
                            if node.type == 'Slack':
                                PGi = (node.P_INJ-node.P_s + node.PLi).item()
                                QGi = node.Q_INJ-node.Q_s-node.Q_s_fx+node.QLi

                            if node.type == 'PV':
                                QGi = node.Q_INJ -(node.Q_s+node.Q_s_fx)+node.QLi

                            table.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(node.QLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.P_s*self.Grid.S_base, decimals=self.dec).item(), np.round((node.Q_s+node.Q_s_fx)*self.Grid.S_base, decimals=self.dec).item(), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec)])
                            table_all.add_row([node.name, np.round(PGi*self.Grid.S_base, decimals=self.dec), np.round(QGi*self.Grid.S_base, decimals=self.dec), np.round(node.PLi*self.Grid.S_base, decimals=self.dec), np.round(node.QLi*self.Grid.S_base, decimals=self.dec), np.round(
                                node.P_s*self.Grid.S_base, decimals=self.dec).item(), np.round((node.Q_s+node.Q_s_fx)*self.Grid.S_base, decimals=self.dec).item(), np.round(node.P_INJ*self.Grid.S_base, decimals=self.dec), np.round(node.Q_INJ*self.Grid.S_base, decimals=self.dec), g+1])

                print(table)
        if self.export == True:
            csv_filename = 'AC_Powerflow.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def AC_voltage(self):
        print('--------------')
        print(f'Results AC bus voltage')
        print('')
        table_all = pt()
        table_all.field_names = [
            "Bus", "Voltage (pu)", "Voltage angle (deg)", "Grid"]

        for g in range(self.Grid.Num_Grids_AC):
            print(f'Grid AC {g+1}')
            table = pt()

            table.field_names = ["Bus", "Voltage (pu)", "Voltage angle (deg)"]

            for node in self.Grid.nodes_AC:
                if self.Grid.Graph_node_to_Grid_index_AC[node.nodeNumber] == g:
                    table.add_row([node.name, np.round(node.V, decimals=self.dec), np.round(
                        np.degrees(node.theta), decimals=self.dec)])
                    table_all.add_row([node.name, np.round(node.V, decimals=self.dec), np.round(
                        np.degrees(node.theta), decimals=self.dec), g+1])

            if len(table.rows) > 0:  # Check if the table is not None and has at least one row
                print(table)

        if self.export == True:
            csv_filename = 'AC_voltage.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def AC_lines_current(self):
        
        print('--------------')
        print(f'Results AC Lines Currents')
        table_all = pt()
        table_all.field_names = ["Line", "From bus", "To bus",
                                 "i from (kA)", "i to (kA)", "Loading %", "Grid"]
        for g in range(self.Grid.Num_Grids_AC):
            print(f'Grid AC {g+1}')
            tablei = pt()
            tablei.field_names = ["Line", "From bus", "To bus",
                                  "i from (kA)", "i to (kA)", "Loading %"]

            for line in self.Grid.lines_AC:
                if self.Grid.Graph_line_to_Grid_index_AC[line] == g:
                    i = line.fromNode.nodeNumber
                    j = line.toNode.nodeNumber
                    I_base = self.Grid.S_base/line.V_base

                    i_from = self.Grid.Iij_AC[i, j]*I_base/np.sqrt(3)
                    p_from = self.Grid.Pij_AC[i, j]*self.Grid.S_base
                    Q_from = self.Grid.Qij[i, j]*self.Grid.S_base

                    i_to = self.Grid.Iij_AC[j, i]*I_base/np.sqrt(3)
                    p_to = self.Grid.Pij_AC[j, i]*self.Grid.S_base
                    Q_to = self.Grid.Qij[j, i]*self.Grid.S_base

                    Sfrom = abs(self.Grid.Sij[i, j]*self.Grid.S_base)
                    Sto = abs(self.Grid.Sij[j, i]*self.Grid.S_base)

                    load = max(Sfrom, Sto)/line.MVA_rating*100

                    Ploss = np.real(line.loss)*self.Grid.S_base
                    Qloss = np.imag(line.loss)*self.Grid.S_base

                    tablei.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        i_from, decimals=self.dec), np.round(i_to, decimals=self.dec), np.round(load, decimals=self.dec)])
                    table_all.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        i_from, decimals=self.dec), np.round(i_to, decimals=self.dec), np.round(load, decimals=self.dec), g+1])
            if len(tablei.rows) > 0:  # Check if the table is not None and has at least one row
                print(tablei)

        if self.export == True:
            csv_filename = 'AC_line_current.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def AC_lines_power(self, Grid=None):
        
        print('--------------')
        print(f'Results AC Lines power')
        table_all = pt()
        table_all.field_names = ["Line", "From bus", "To bus",
                                 "P from (MW)", "Q from (MVAR)", "P to (MW)", "Q to (MW)", "Power loss (MW)", "Q loss (MVAR)", "Grid"]

        for g in range(self.Grid.Num_Grids_AC):
            if Grid == (g+1):
                print(f'Grid AC {g+1}')

                tablep = pt()
                tablep.field_names = ["Line", "From bus", "To bus",
                                      "P from (MW)", "Q from (MVAR)", "P to (MW)", "Q to (MW)", "Power loss (MW)", "Q loss (MVAR)"]

                for line in self.Grid.lines_AC:
                    if self.Grid.Graph_line_to_Grid_index_AC[line] == g:
                        i = line.fromNode.nodeNumber
                        j = line.toNode.nodeNumber
                        I_base = self.Grid.S_base/line.V_base

                        i_from = self.Grid.Iij_AC[i, j]*I_base/np.sqrt(3)
                        p_from = self.Grid.Pij_AC[i, j]*self.Grid.S_base
                        Q_from = self.Grid.Qij[i, j]*self.Grid.S_base

                        i_to = self.Grid.Iij_AC[j, i]*I_base/np.sqrt(3)
                        p_to = self.Grid.Pij_AC[j, i]*self.Grid.S_base
                        Q_to = self.Grid.Qij[j, i]*self.Grid.S_base

                        Sfrom = abs(self.Grid.Sij[i, j]*self.Grid.S_base)
                        Sto = abs(self.Grid.Sij[j, i]*self.Grid.S_base)

                        load = max(Sfrom, Sto)/line.MVA_rating*100
                        
                        Ploss = np.real(line.loss)*self.Grid.S_base
                        Qloss = np.imag(line.loss)*self.Grid.S_base

                        tablep.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(p_from, decimals=self.dec), np.round(Q_from, decimals=self.dec), np.round(
                            p_to, decimals=self.dec), np.round(Q_to, decimals=self.dec), np.round(Ploss, decimals=self.dec), np.round(Qloss, decimals=self.dec)])

            elif Grid == None:

                print(f'Grid AC {g+1}')

                tablep = pt()
                tablep.field_names = ["Line", "From bus", "To bus",
                                      "P from (MW)", "Q from (MVAR)", "P to (MW)", "Q to (MW)", "Power loss (MW)", "Q loss (MVAR)"]

                for line in self.Grid.lines_AC:
                    if self.Grid.Graph_line_to_Grid_index_AC[line] == g:
                        i = line.fromNode.nodeNumber
                        j = line.toNode.nodeNumber
                        I_base = self.Grid.S_base/line.V_base

                        i_from = self.Grid.Iij_AC[i, j]*I_base/np.sqrt(3)
                        p_from = self.Grid.Pij_AC[i, j]*self.Grid.S_base
                        Q_from = self.Grid.Qij[i, j]*self.Grid.S_base

                        i_to = self.Grid.Iij_AC[j, i]*I_base/np.sqrt(3)
                        p_to = self.Grid.Pij_AC[j, i]*self.Grid.S_base
                        Q_to = self.Grid.Qij[j, i]*self.Grid.S_base

                        Sfrom = abs(self.Grid.Sij[i, j]*self.Grid.S_base)
                        Sto = abs(self.Grid.Sij[j, i]*self.Grid.S_base)

                        load = max(Sfrom, Sto)/line.MVA_rating*100

                        Ploss = np.real(line.loss)*self.Grid.S_base
                        Qloss = np.imag(line.loss)*self.Grid.S_base

                        tablep.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(p_from, decimals=self.dec), np.round(Q_from, decimals=self.dec), np.round(
                            p_to, decimals=self.dec), np.round(Q_to, decimals=self.dec), np.round(Ploss, decimals=self.dec), np.round(Qloss, decimals=self.dec)])
                        table_all.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(p_from, decimals=self.dec), np.round(Q_from, decimals=self.dec), np.round(
                            p_to, decimals=self.dec), np.round(Q_to, decimals=self.dec), np.round(Ploss, decimals=self.dec), np.round(Qloss, decimals=self.dec), g+1])

                if len(tablep.rows) > 0:  # Check if the table is not None and has at least one row
                    print(tablep)

        if self.export == True:
            csv_filename = 'AC_line_power.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)
    def Ext_gen(self):
        print('--------------')
        print(f'External Generation optimization')
        table = pt()
        Ptot=0
        Qtot=0
        Pabs=0
        Qabs=0
        Stot=0
        Ltot=0
        costtot=0
        table.field_names = ["Bus", "Power (MW)", "Reactive power (MVAR)","Price €/MWh","Loading %","Cost k€"]
        for node in self.Grid.nodes_AC:
            if node.extGrid == 1 or node.extGrid == 2:
                Pgi=node.PGi_opt #+node.PGi*node.curtailment
                if node.extGrid == 1:
                    Pgi=0
                Qgi=node.QGi_opt
                S= np.sqrt(Pgi**2+Qgi**2)
                Pgi*=self.Grid.S_base
                Qgi*=self.Grid.S_base
                if node.extGrid ==2:
                    load=S/node.Max_pow_gen*100
                    cost=Pgi*node.price/1000
                else:
                    load=S/np.abs(node.Min_pow_genR)*100
                    cost=0
                    
                table.add_row([node.name, np.round(Pgi, decimals=self.dec), np.round(Qgi, decimals=self.dec),  np.round(node.price, decimals=self.dec),np.round(load, decimals=self.dec), np.round(cost, decimals=0)])
                Pabs+=abs(Pgi)
                Qabs+=abs(Qgi)
                Ptot+=Pgi
                Qtot+=Qgi
                Stot+=S
                costtot+=cost
                Ltot+=node.Max_pow_gen
                
        if Ltot !=0:
            load=Stot/Ltot*100
        else:
            load=0
        table.add_row(['Total', np.round(Ptot, decimals=self.dec), np.round(Qtot, decimals=self.dec),""," ", np.round(costtot, decimals=0)])
        table.add_row(['Total abs', np.round(Pabs, decimals=self.dec), np.round(Qabs, decimals=self.dec), "",np.round(load, decimals=self.dec),""])
        print(table)
    
    def Ext_WPP(self):
        print('--------------')
        print('Renewable energy sources')
        table = pt()
        table.field_names = ["Bus", "Base Power (MW)", "Curtailment %","Power Injected (MW)","Price €/MWh","Cost k€","Curtailment Cost [k€]"]
        bp=0
        tcur=0
        totcost=0
        totcurcost=0
        for node in self.Grid.nodes_AC:
            if node.RenSource == True:
                Pgi=node.PGi_ren*self.Grid.S_base
                bp+=Pgi
                cur= (1-node.curtailment)*100
                tcur+=Pgi*(1-node.curtailment)
                PGicur=Pgi*(node.curtailment)
            
                
                if self.Grid.OnlyGen==True:
                    cost=0
                else:
                    cost= PGicur*node.price/1000
                if self.Grid.CurtCost==False:
                    curcost=0
                else:    
                    curcost= (Pgi-PGicur)*node.price*(self.Grid.sigma)/1000
                table.add_row([node.name, np.round(Pgi, decimals=self.dec), np.round(cur, decimals=self.dec),  np.round(PGicur, decimals=self.dec),np.round(node.price, decimals=self.dec),np.round(cost, decimals=0),np.round(curcost, decimals=0)])
                totcost+=cost
                totcurcost+=curcost
        
     
        
        PGicur=bp-tcur
        cur=(tcur)/bp*100
        
        table.add_row(['Total', np.round(bp, decimals=self.dec), np.round(cur, decimals=self.dec),  np.round(PGicur, decimals=self.dec) ,"",np.round(totcost, decimals=0),np.round(totcurcost, decimals=0)])

        print(table)    
    
    def Market(self):
        print('--------------')
        print('Market')
        table = pt()
        table.field_names = ["Market","Renewable Generation(MW)" ,"Generation (MW)", "Load (MW)","Import (MW)","Export (MW)","Price (€/MWh)"]
        table2 = pt()
        table2.field_names = ["Market","Social Cost [k€]","Renewable Gen Cost [k€]","Curtailent Cost [k€]","Generation Cost [k€]","Total Cost [k€]"]
        
        tot_sc=0
        tot_Rgen_cost=0
        tot_gen_cost=0
        tot_curt_cost=0
        tot_m_tot=0
        
        
        for m in self.Grid.Markets:
            Rgendisp= sum(node.PGi_ren for node in m.nodes_AC)*self.Grid.S_base
            Rgen = sum(node.PGi_ren*node.curtailment for node in m.nodes_AC)*self.Grid.S_base
            gen = sum(node.PGi+node.PGi_opt for node in m.nodes_AC)*self.Grid.S_base
            load = sum(node.PLi for node in m.nodes_AC)*self.Grid.S_base
            ie = Rgen+gen-load
            price=m.price
            
            
            
            sc = (m.a*ie**2+ie*m.b)/1000
            
            if self.Grid.OnlyGen==True:
                Rgen_cost=0
            else:
                Rgen_cost= Rgen*m.price/1000          
            gen_cost = gen*m.price/1000
            if self.Grid.CurtCost==False:
                curt_cost=0
            else:  
                curt_cost= (Rgendisp-Rgen)*m.price*(self.Grid.sigma)/1000
            m_tot= Rgen_cost+gen_cost+curt_cost+sc
            
            tot_sc+=sc
            tot_Rgen_cost+=Rgen_cost
            tot_gen_cost+=gen_cost
            tot_curt_cost+=curt_cost
            tot_m_tot+=m_tot
            
            if ie >=0:
                export = ie
                imp = 0
            else: 
                export = 0
                imp = abs(ie)
            table.add_row([m.name,  np.round(Rgen, decimals=self.dec),np.round(gen, decimals=self.dec), np.round(load, decimals=self.dec),  np.round(imp, decimals=self.dec),np.round(export, decimals=self.dec),np.round(price, decimals=2)])
            table2.add_row([m.name,  np.round(sc, decimals=self.dec),np.round(Rgen_cost, decimals=self.dec), np.round(curt_cost, decimals=self.dec),  np.round(gen_cost, decimals=self.dec),np.round(m_tot, decimals=self.dec)])
        
        
        if len(table.rows) > 0:  # Check if the table is not None and has at least one row
            table2.add_row(['Total',  np.round(tot_sc, decimals=self.dec),np.round(tot_Rgen_cost, decimals=self.dec), np.round(tot_curt_cost, decimals=self.dec),  np.round(tot_gen_cost, decimals=self.dec),np.round(tot_m_tot, decimals=self.dec)])
            print(table)
            print(table2)
            
            
    
    def DC_lines_current(self):
        
        print('--------------')
        print(f'Results DC Lines current')
        table_all = pt()
        table_all.field_names = [
            "Line", "From bus", "To bus", "I (kA)", "Loading %", "Polarity", "Grid"]
        for g in range(self.Grid.Num_Grids_DC):
            print(f'Grid DC {g+1}')
            tablei = pt()

            tablei.field_names = ["Line", "From bus",
                                  "To bus", "I (kA)", "Loading %", "Polarity"]
            tablei.align["Polarity"] = 'l'

            for line in self.Grid.lines_DC:
                if self.Grid.Graph_line_to_Grid_index_DC[line] == g:

                    i = line.fromNode.nodeNumber
                    j = line.toNode.nodeNumber
                    I_base = self.Grid.S_base/line.V_base
                    i_to = self.Grid.Iij_DC[j, i]*I_base

                    p_to = self.Grid.Pij_DC[j, i]*self.Grid.S_base
                    p_from = self.Grid.Pij_DC[i, j]*self.Grid.S_base

                    load = max(p_to, p_from)/line.MW_rating*100

                    if line.m_sm_b == 'm':
                        pol = "Monopolar (asymmetrically grounded)"
                    elif line.m_sm_b == 'sm':
                        pol = "Monopolar (symmetrically grounded)"
                    elif line.m_sm_b == 'b':
                        pol = "Bipolar"
                    Ploss = np.real(line.loss)*self.Grid.S_base

                    tablei.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        i_to, decimals=self.dec), np.round(load, decimals=self.dec), pol])
                    table_all.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        i_to, decimals=self.dec), np.round(load, decimals=self.dec), pol, g+1])

            if len(tablei.rows) > 0:  # Check if the table is not None and has at least one row
                print(tablei)

        if self.export == True:
            csv_filename = 'DC_line_current.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)
                
    def DC_lines_power(self):
        
        print('--------------')
        print(f'Results DC Lines power')
        table_all = pt()
        table_all.field_names = ["Line", "From bus", "To bus",
                                 "P from (MW)", "P to (MW)", "Power loss (MW)", "Grid"]
        for g in range(self.Grid.Num_Grids_DC):
            print(f'Grid DC {g+1}')
            tablep = pt()
            tablep.field_names = ["Line", "From bus", "To bus",
                                  "P from (MW)", "P to (MW)", "Power loss (MW)"]

            for line in self.Grid.lines_DC:
                if self.Grid.Graph_line_to_Grid_index_DC[line] == g:
                    i = line.fromNode.nodeNumber
                    j = line.toNode.nodeNumber
                    I_base = self.Grid.S_base/line.V_base
                    i_to = self.Grid.Iij_DC[j, i]*I_base

                    p_to = self.Grid.Pij_DC[j, i]*self.Grid.S_base
                    p_from = self.Grid.Pij_DC[i, j]*self.Grid.S_base

                    load = max(p_to, p_from)/line.MW_rating*100

                    if line.pol == 1:
                        pol = "monopolar (asymmetrically grounded)"
                    elif line.pol == 2:
                        pol = "monopolar (symmetrically grounded) or bipolar"
                    Ploss = np.real(line.loss)*self.Grid.S_base

                    tablep.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        p_from, decimals=self.dec), np.round(p_to, decimals=self.dec), np.round(Ploss, decimals=self.dec)])
                    table_all.add_row([line.name, line.fromNode.name, line.toNode.name, np.round(
                        p_from, decimals=self.dec), np.round(p_to, decimals=self.dec), np.round(Ploss, decimals=self.dec), g+1])

            if len(tablep.rows) > 0:  # Check if the table is not None and has at least one row
                print(tablep)

        if self.export == True:
            csv_filename = 'DC_line_power.csv'
            csv_data = table_all.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def Converter(self):
        table = pt()
        table2 = pt()
        table.field_names = ["Converter", "AC node", "DC node","Power s AC (MW)","Reactive s AC (MVAR)", "Power c AC (MW)", "Power DC(MW)", "Reactive power (MVAR)", "Power loss IGBTs (MW)", "Power loss AC elements (MW)"]
        table2.field_names = ["Converter","AC control mode", "DC control mode","Loading %"]
        for conv in self.Grid.Converters_ACDC:
            if conv.type == 'Slack':
                P_DC = np.round(conv.Node_DC.P*self.Grid.S_base,
                                decimals=self.dec)
            else:
                P_DC = np.round(conv.P_DC*self.Grid.S_base, decimals=self.dec)
            P_s = np.round(conv.P_AC*self.Grid.S_base, decimals=self.dec)
            Q_s = np.round(conv.Q_AC*self.Grid.S_base, decimals=self.dec)
            P_c = np.round(conv.Pc*self.Grid.S_base, decimals=self.dec)
            Q_c = np.round(conv.Qc*self.Grid.S_base, decimals=self.dec)
            P_loss = np.round(conv.P_loss*self.Grid.S_base, decimals=self.dec)
            Ploss_tf = np.round(conv.P_loss_tf*self.Grid.S_base, decimals=self.dec)
            S = np.sqrt(P_s**2+Q_s**2)
            
            loading= np.round(max(S,abs(P_DC))/conv.MVA_max*100, decimals=self.dec)
            table.add_row([conv.name, conv.Node_AC.name,
                          conv.Node_DC.name, P_s,Q_s ,P_c, P_DC, Q_c, P_loss, Ploss_tf])
            table2.add_row([conv.name, conv.AC_type, conv.type,loading])

        print('------------')
        print('AC DC Converters')
        if len(table.rows) > 0:  # Check if the table is not None and has at least one row
            print(table)
            print(table2)

        if self.export == True:
            csv_filename = 'Converter_results.csv'
            csv_data = table.get_csv_string()

            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(csv_data)

    def Time_series_prob(self, element_name):
        a = self.Grid.Time_series
        b = self.Grid.lines_AC
        c = self.Grid.lines_DC

        df_res = self.Grid.Time_series_res
        df_line_res = self.Grid.Time_series_line_res
        df_grid_res = self.Grid.Time_series_grid_res

        if self.Grid.VarPrice == True:
            merged_df = pd.concat([df_res, df_line_res, df_grid_res,self.Grid.Time_series_price], axis=1)
        else:
            merged_df = pd.concat([df_res, df_line_res, df_grid_res], axis=1)

        for ts in a:
            if ts.type != 'Slack':
                if ts.name == element_name:

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

                    # Plot PDF
                    ax1.hist(ts.TS, bins=100, density=True,
                             alpha=0.5, color='b')
                    ax1.set_title('Probability Density Function (PDF)')
                    ax1.set_xlabel(ts.name)
                    ax1.set_ylabel('Probability')

                    # Plot CDF
                    sorted_data = np.sort(ts.TS)
                    cumulative_prob = np.linspace(0, 1, len(sorted_data))

                    # Plot the CDF as a line
                    ax2.plot(sorted_data, cumulative_prob,
                             marker='.', linestyle='-')
                    ax2.set_title('Cumulative Distribution Function (CDF)')
                    ax2.set_xlabel(ts.name)
                    ax2.set_ylabel('Probability')

                    plt.show()

        for col in merged_df.columns:
            if col.startswith(element_name) or col.endswith(element_name):
                # Assuming a normal distribution

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

                # Plot PDF
                ax1.hist(merged_df[col], bins=100,
                         density=True, alpha=0.5, color='b')
                ax1.set_title('Probability Density Function (PDF)')
                ax1.set_xlabel(col)
                ax1.set_ylabel('Probability')

                # Plot CDF
                sorted_data = np.sort(merged_df[col])
                cumulative_prob = np.linspace(0, 1, len(sorted_data))

                # Plot the CDF as a line
                ax2.plot(sorted_data, cumulative_prob,
                         marker='.', linestyle='-')
                ax2.set_title('Cumulative Distribution Function (CDF)')
                ax2.set_xlabel(col)
                ax2.set_ylabel('Probability')

                plt.show()

    def Time_series_plots(self, start=1, end=9999,All=False):

        if self.Grid.Time_series_res.index[-1] < end:
            end = self.Grid.Time_series_res.index[-1]

        if self.Grid.Time_series_res.index[0] > start:
            start = self.Grid.Time_series_res.index[0]

        s = 1

        genPg = [ts.name for ts in self.Grid.Time_series if (ts.type != 'Slack' and ts.type != 'Load')]
        s = 1
        self.Grid.Time_series_input.loc[start+1:end+1,genPg].plot(kind='line', title='Power fixed generation')
        plt.xlabel('Time')
        plt.ylabel('PG Value (pu)')
        plt.legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

        LoadPg = [ts.name for ts in self.Grid.Time_series if ts.type == 'Load']
        self.Grid.Time_series_input.loc[start+1:end+1,
                                        LoadPg].plot(kind='line', title='Power Load')
        plt.xlabel('Time')
        plt.ylabel('Load Value (pu)')
        plt.legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

        if self.Grid.VarPrice == True:
            price = [col for col in self.Grid.Time_series_price.columns]
            s = 1
            self.Grid.Time_series_price.loc[start+1:end+1, price].plot(
                kind='line', title='Price in different markets')
            plt.xlabel('Time')
            plt.ylabel('Price (Eu/pu)')
            plt.legend(title='Source', bbox_to_anchor=(
                1.05, 1), loc='upper left')
            plt.show()

          

        # Plotting Pg for Slack nodes
        slack_colsPg_ = [
            col for col in self.Grid.Time_series_res.columns if 'Pg_' in col]
        self.Grid.Time_series_res.loc[start:end, slack_colsPg_].plot(
            kind='line', title='Power generation')
        plt.xlabel('Time')
        plt.ylabel('PG Value (pu)')
        plt.legend(title='Node', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

        # Plotting Qg for Slack nodes
        slack_colsQg_ = [
            col for col in self.Grid.Time_series_res.columns if 'Qg_' in col]
        self.Grid.Time_series_res.loc[start:end, slack_colsQg_].plot(
            kind='line', title='Reactive power generation')
        plt.xlabel('Time')
        plt.ylabel('QG Value (pu)')
        plt.legend(title='Node', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

        # Plotting max for Converters
        converter_cols = [
            col for col in self.Grid.Time_series_res.columns if '_max' in col]
        self.Grid.Time_series_res.loc[start:end, converter_cols].plot(
            kind='line', title='Maximum power in each Converter')
        plt.xlabel('Time')
        plt.ylabel('Maximum power')
        plt.legend(title='Converter', bbox_to_anchor=(
            1.05, 1), loc='upper left')
        plt.show()

        # Plotting PDC for Converters
        converter_cols = [
            col for col in self.Grid.Time_series_res.columns if '_P_DC' in col]
        self.Grid.Time_series_res.loc[start:end, converter_cols].plot(
            kind='line', title='DC power in each Converter')
        plt.xlabel('Time')
        plt.ylabel('DC power')
        plt.legend(title='Converter', bbox_to_anchor=(
            1.05, 1), loc='upper left')
        plt.show()
        
        if All ==True:
            # Plotting AC line Loads
            line_cols = [
                col for col in self.Grid.Time_series_line_res.columns if 'Load_AC_' in col]
            line_load_data = self.Grid.Time_series_line_res.loc[start:end, line_cols]
    
            # Remove "Load_AC_" from legend labels
            legend_labels = [col.replace('Load_AC_', '') for col in line_cols]
    
            line_load_data.plot(kind='line', title='Power load in each AC Line')
            plt.xlabel('Time')
            plt.ylabel('Line load (pu of power)')
            plt.legend(title='Line', labels=legend_labels,
                       bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.show()
    
            # Plotting DC line Loads
            line_cols = [
                col for col in self.Grid.Time_series_line_res.columns if 'Load_DC_' in col]
            line_load_data = self.Grid.Time_series_line_res.loc[start:end, line_cols]
    
            # Remove "Load_DC_" from legend labels
            legend_labels = [col.replace('Load_DC_', '') for col in line_cols]
    
            line_load_data.plot(kind='line', title='Power load in each  DC Line')
            plt.xlabel('Time')
            plt.ylabel('Line load (pu of power)')
            plt.legend(title='Line', labels=legend_labels,
                       bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.show()
    
            # Plotting AC line Loads
            line_cols = [
                col for col in self.Grid.Time_series_line_res.columns if 'Loss_AC_' in col]
            line_load_data = self.Grid.Time_series_line_res.loc[start:end, line_cols]
    
            # Remove "Load_AC_" from legend labels
            legend_labels = [col.replace('Loss_AC_', '') for col in line_cols]
    
            line_load_data.plot(kind='line', title='Power loss in each AC Line')
            plt.xlabel('Time')
            plt.ylabel('Line load (pu of power)')
            plt.legend(title='Line', labels=legend_labels,
                       bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.show()
    
            # Plotting DC line Loads
            line_cols = [
                col for col in self.Grid.Time_series_line_res.columns if 'Loss_DC_' in col]
            line_load_data = self.Grid.Time_series_line_res.loc[start:end, line_cols]
    
            # Remove "Load_AC_" from legend labels
            legend_labels = [col.replace('Loss_DC_', '') for col in line_cols]
    
            line_load_data.plot(kind='line', title='Power loss in each DC Line')
            plt.xlabel('Time')
            plt.ylabel('Line load (pu of power)')
            plt.legend(title='Line', labels=legend_labels,
                       bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.show()
    
            # Plotting line loss for each grid
            grid_cols = [col for col in self.Grid.Time_series_grid_res.columns]
            self.Grid.Time_series_grid_res.loc[start:end, grid_cols].plot(
                kind='line', title='Power loss in each Grid')
            plt.xlabel('Time')
            plt.ylabel('Grid loss (pu of power)')
            plt.legend(title='Grid', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.show()
