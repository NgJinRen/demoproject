FusionCharts.ready(function(){
    var chartObj = new FusionCharts({
        type: 'pie2d',
        renderAt: 'chart-donut-2016',
        containerBackgroundOpacity: '0',
        width: '100%',
        height: '100',
        dataFormat: 'json',
        creditLabel: false,
        dataSource: {
            "chart": {   
                "bgColor": "#ffffff",        
                "labelFontColor":"#FFFFFF",         
                "startingAngle": "180",
                "showLegend": "0",
                "centerLabelBold": "1",
                "showTooltip": "0",
                "bgAlpha":"0",
                "decimals": "0",
                "theme": "fusion"
            },
            "data": [{
                "label": "Positive",
                "value":"123"
            }, {
                "label": "Negative",
                "value":"345"
            },{
              "label": "Neutral",
              "value":"44343"
          }]
        }
    });
    chartObj.render();
  });