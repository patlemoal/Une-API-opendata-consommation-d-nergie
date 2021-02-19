Highcharts.chart('container', {
    data: {
      table: 'datatable'
    },
    chart: {
      type: 'column'
    },
    title: {
      text: 'Consommation de Gaz et d\'Electricité de la région'
    },
    yAxis: {
      allowDecimals: false,
      title: {
        text: 'MW/h'
      }
    },
    tooltip: {
      formatter: function () {
        return '<b>' + this.series.name + '</b><br/>' +
          this.point.y + ' ' + this.point.name.toLowerCase();
      }
    }
  });