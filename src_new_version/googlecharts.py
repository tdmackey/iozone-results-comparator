#!/usr/bin/python

#   Copyright (C) 2013
#   Adam Okuliar        aokuliar at redhat dot com
#   Jiri Hladky         hladky dot jiri at gmail dot com
#   Petr Benas          petrbenas at gmail dot com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
from jinja2 import Template

class GoogleCharts:
    def __init__(self):
        self.opnames={"iwrite":"Write", "rewrite":"Re-write", "iread":"Read",
        "reread":"Re-read", "randrd":"Random read", "randwr":"Random write",
        "bkwdrd":"Backwards read", "recrewr":"Record rewrite", "striderd":"Strided Read",
        "fwrite":"Fwrite","frewrite":"Frewrite", "fread":"Fread", "freread":"Freread", "ALL":"ALL"}

        self.normTemplate = Template('''<script type="text/javascript">
            // Load the Visualization API and the piechart package.
            google.load('visualization', '1.0', {'packages':['corechart']});
            // Set a callback to run when the Google Visualization API is loaded.
            google.setOnLoadCallback(drawChart);
            // Callback that creates and populates a data table, 
            // instantiates the chart, passes in the data and draws it.
            function drawChart() {
                var data = new google.visualization.DataTable();
                data.addColumn('string', 'This does not matter'); // Implicit domain label col.
                data.addColumn('number', 'baseline'); // Implicit series 1 data col.
                data.addColumn({type:'number', role:'interval', label:'Bar'});  // interval role col.
                data.addColumn({type:'number', role:'interval'});  // interval role col.
                data.addColumn('number', 'set1'); // Implicit series 1 data col.
                data.addColumn({type:'number', role:'interval'});  // interval role col.
                data.addColumn({type:'number', role:'interval'});  // interval role col.
                data.addRows({{ dataRows }});
            // Set chart options
            var options = {title : '{{ title }}', colors : ['black', 'red'],
                focusTarget : 'category', vAxis : {title : 'Operation speed [MB/s]'},
                hAxis : {title : '{{ xlabel }}', textStyle : {fontSize : 9}}};
            // Instantiate and draw our chart, passing in some options.
            var chart = new google.visualization.LineChart(document.getElementById('{{ id }}'));
            chart.draw(data, options);
        }
        </script>''')
        
    def norm_plot(self, Op, Source):
        # columns have following meanding:
        # xAxisLabel, baseline median, base errbar low, base errbar high, set1 median, set1 errbar low, set1 errbar high
        dataRows = []
        
        x = 4
        for i in range(0, len(Source.base[Op].medians)):
            dataRows.append([str(x), round(Source.base[Op].medians[i], 2),
                round(Source.base[Op].first_qrts[i], 2),
                round(Source.base[Op].third_qrts[i], 2), round(Source.set1[Op].medians[i], 2),
                round(Source.set1[Op].first_qrts[i], 2), round(Source.set1[Op].third_qrts[i], 2)])
            x = x*2

        return self.normTemplate.render(id = Op + '_' + Source.base[Op].datatype,
                title = self.opnames[Op], xlabel = Source.base[Op].xlabel, 
                dataRows = json.dumps(dataRows))

if __name__ == '__main__':
    print 'Try running iozone_results_comparator.py'

