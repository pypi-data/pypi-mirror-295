function support_scientific_notation(option) {
  if (Array.isArray(option['yAxis'])) {
    for (var tar_ind = 0; tar_ind < option['yAxis'].length; tar_ind++) {
      if (option['yAxis'][tar_ind]['type'] === 'value') {
        option['yAxis'][tar_ind]['axisLabel']['formatter'] = function(val) {
          const superscripts = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹','¹⁰',
                    '¹¹', '¹²', '¹³', '¹⁴', '¹⁵', '¹⁶', '¹⁷', '¹⁸', '¹⁹','²⁰',
                    '²¹', '²²', '²³', '²⁴', '²⁵', '²⁶', '²⁷', '²⁸', '²⁹'];
          function toSuperscript(val) {
            if (val.toString().length > 5 && !val.toString().includes('.')) {
              val = Number(val).toExponential().toString();
              if (val.includes('-')) {
                val = val.split('-');
                var val0 = val[0];
                var val1 = superscripts[val[1]];
                return val0 + '⁻' + val1
              }
              else if (val.includes('+')) {
                val = val.split('+');
                var val0 = val[0];
                var val1 = superscripts[val[1]];
                return val0 + '⁺' + val1
              }
            }
            else {
              return val
            }
          }
          return toSuperscript(val)
        }
      }
    }
  }
  else {
    if (option['yAxis']['type'] === 'value') {
      option['yAxis']['axisLabel']['formatter'] = function(val) {
        const superscripts = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹','¹⁰',
                '¹¹', '¹²', '¹³', '¹⁴', '¹⁵', '¹⁶', '¹⁷', '¹⁸', '¹⁹','²⁰',
                '²¹', '²²', '²³', '²⁴', '²⁵', '²⁶', '²⁷', '²⁸', '²⁹'];
        function toSuperscript(val) {
          if (val.toString().length > 5 && !val.toString().includes('.')) {
            val = Number(val).toExponential().toString();
            if (val.includes('-')) {
              val = val.split('-');
              var val0 = val[0];
              var val1 = superscripts[val[1]];
              return val0 + '⁻' + val1
            }
            else if (val.includes('+')) {
              val = val.split('+');
              var val0 = val[0];
              var val1 = superscripts[val[1]];
              return val0 + '⁺' + val1
            }
          }
          else {
            return val
          }
        }
        return toSuperscript(val)
      }
    }
  };
  return option;
};

function save_img(echarts_instance, option) {
  const base64_str = echarts_instance.getDataURL({
      pixelRatio: 2,
      backgroundColor: '#fff'
  });

  let testRequest = new Request('http://localhost:' + option['port'] +'/function/js_image_save', {
    method: 'post',
    headers: {
      'Content-Type': 'application/json;charset=utf-8;',
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Credentials': 'true',
      'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
    },
    body: JSON.stringify({'figname': option['figname'],
                          'base64_str': base64_str})
  });
  fetch(testRequest).then(response => {});
};


function auto_axis_namegap(echarts_instance, auto_axis_list, axis_type) {
  const globalModel = echarts_instance._api.getModel()
  const figsize = globalModel.option.figsize
  const ctx = document.createElement('canvas').getContext('2d')
  if (axis_type==='2d') {
    const yAxisList = globalModel.option.yAxis
    const xAxisList = globalModel.option.xAxis

    for (var axis_idx of auto_axis_list) {
      const yAxis = yAxisList[axis_idx]
      const fontSize = yAxis.nameTextStyle?.fontSize ?? 12
      const fontFamily = yAxis.nameTextStyle?.fontFamily ?? 'sans-serif'
      ctx.save()
      ctx.font = fontSize.toString() + 'px' + fontFamily.toString()
  
      const yAxisComponent = globalModel.getComponent('yAxis', axis_idx)?.axis
      if (yAxis.type === 'value') {
        var labelMaxWidth = Math.min(Math.max(...yAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width)), 30)
      }
      else {
        var labelMaxWidth = Math.max(...yAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width))
      }
      const axisLabelMargin = yAxis.axisLabel?.margin ?? 8
      yAxisList[axis_idx].nameGap = labelMaxWidth + axisLabelMargin + 5
      ctx.restore()
    };
  
    for (var axis_idx of [...Array(xAxisList.length).keys()]) {
      if (figsize['height'] < 400) {
        xAxisList[axis_idx].nameGap = Math.min(20, xAxisList[axis_idx].nameGap)
      }
    }
  
    echarts_instance.setOption({
      yAxis: yAxisList,
      xAxis: xAxisList
    })
  }
  else {
    const yAxisList = globalModel.option.yAxis3D
    const xAxisList = globalModel.option.xAxis3D
    const zAxisList = globalModel.option.zAxis3D

    for (var axis_idx of auto_axis_list) {
      if (axis_idx < xAxisList.length) {
        const xAxis = xAxisList[axis_idx]
        const fontSize = xAxis.nameTextStyle?.fontSize ?? 12
        const fontFamily = xAxis.nameTextStyle?.fontFamily ?? 'sans-serif'
        ctx.save()
        ctx.font = fontSize.toString() + 'px' + fontFamily.toString()
    
        const xAxisComponent = globalModel.getComponent('xAxis3D', axis_idx)?.axis
        if (xAxis.type === 'value') {
          var labelMaxWidth = Math.min(Math.max(...xAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width)), 30)
        }
        else {
          var labelMaxWidth = Math.max(...xAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width))
        }
        const axisLabelMargin = xAxis.axisLabel?.margin ?? 8
        xAxisList[axis_idx].nameGap = labelMaxWidth + axisLabelMargin + 5
        ctx.restore()
      }
    };

    for (var axis_idx of auto_axis_list) {
      if (axis_idx < yAxisList.length) {
        const yAxis = yAxisList[axis_idx]
        const fontSize = yAxis.nameTextStyle?.fontSize ?? 12
        const fontFamily = yAxis.nameTextStyle?.fontFamily ?? 'sans-serif'
        ctx.save()
        ctx.font = fontSize.toString() + 'px' + fontFamily.toString()
    
        const yAxisComponent = globalModel.getComponent('yAxis3D', axis_idx)?.axis
        if (yAxis.type === 'value') {
          var labelMaxWidth = Math.min(Math.max(...yAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width)), 30)
        }
        else {
          var labelMaxWidth = Math.max(...yAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width))
        }
        const axisLabelMargin = yAxis.axisLabel?.margin ?? 8
        yAxisList[axis_idx].nameGap = labelMaxWidth + axisLabelMargin + 5
        ctx.restore()
      }
    };

    for (var axis_idx of auto_axis_list) {
      if (axis_idx < zAxisList.length) {
        const zAxis = zAxisList[axis_idx]
        const fontSize = zAxis.nameTextStyle?.fontSize ?? 12
        const fontFamily = zAxis.nameTextStyle?.fontFamily ?? 'sans-serif'
        ctx.save()
        ctx.font = fontSize.toString() + 'px' + fontFamily.toString()
    
        const zAxisComponent = globalModel.getComponent('zAxis3D', axis_idx)?.axis
        if (zAxis.type === 'value') {
          var labelMaxWidth = Math.min(Math.max(...zAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width)), 30)
        }
        else {
          var labelMaxWidth = Math.max(...zAxisComponent.getViewLabels().map(item => ctx.measureText(item.formattedLabel).width))
        }
        const axisLabelMargin = zAxis.axisLabel?.margin ?? 8
        zAxisList[axis_idx].nameGap = labelMaxWidth + axisLabelMargin + 5
        ctx.restore()
      }
    };
    echarts_instance.setOption({
      yAxis3D: yAxisList,
      xAxis3D: xAxisList,
      zAxis3D: zAxisList
    });
    }
  
  
};

function custom_scatter_size(option) {
  
  for (var ind = 0; ind < option['series'].length; ind++) {
    if (option['series'][ind]['symbolSize'] === 'array_size') {
      var ind_ = option['series'][ind]['data_dict']['size']
      option['series'][ind]['symbolSize'] = function (data) {return data[ind_];}
    }
  }
  return option;
  
};

function show_scatter_label(option) {
  
  for (var ind = 0; ind < option['series'].length; ind++) {
    if (option['series'][ind]['label'] === 'show_label') {
      var ind_ = option['series'][ind]['data_dict']['label']
      option['series'][ind]['label'] = {
        show: true,
        formatter: function (params) {return params.data[ind_]; }
      }
    }
  }
  return option;
};

function hide_min_max_axis_label(option) {
  for (var ind = 0; ind < option['xAxis3D'].length; ind++) {
    if (option['xAxis3D'][ind]['type'] == 'value') {
      var x_min = option['xAxis3D'][ind]['min']
      var x_max = option['xAxis3D'][ind]['max']
      option['xAxis3D'][ind]['axisLabel']['formatter'] = function (value, index) {
        if (value==x_min || value==x_max){}
        else {return value}
      }
    }
  }
  for (var ind = 0; ind < option['yAxis3D'].length; ind++) {
    if (option['yAxis3D'][ind]['type'] == 'value') {  
      var y_min = option['yAxis3D'][ind]['min']
      var y_max = option['yAxis3D'][ind]['max']
      option['yAxis3D'][ind]['axisLabel']['formatter'] = function (value, index) {
        if (value==y_min || value==y_max){}
        else {return value}
      }
    }
  }
  for (var ind = 0; ind < option['zAxis3D'].length; ind++) {
    if (option['zAxis3D'][ind]['type'] == 'value') {
      var z_min = option['zAxis3D'][ind]['min']
      var z_max = option['zAxis3D'][ind]['max']
      option['zAxis3D'][ind]['axisLabel']['formatter'] = function (value, index) {
        if (value==z_min || value==z_max){}
        else {return value}
      }
   }
  }
  return option;
}

function custom_axis_label(option) {
  if (Array.isArray(option['xAxis'])) {
    for (var ind = 0; ind < option['xAxis'].length; ind++) {
      if (option['xAxis'][ind]['axisLabel']['formatter_func']) {
        var f = new Function(option['xAxis'][ind]['axisLabel']['formatter_func'].arguments,
                             option['xAxis'][ind]['axisLabel']['formatter_func'].body)
        option['xAxis'][ind]['axisLabel']['formatter'] = f
      }
    }
  }
  else {
    if (option['xAxis']['axisLabel']['formatter_func']) {
      var f = new Function(option['xAxis']['axisLabel']['formatter_func'].arguments,
                           option['xAxis']['axisLabel']['formatter_func'].body)
      option['xAxis']['axisLabel']['formatter'] = f
    }
  }
  if (Array.isArray(option['yAxis'])) {
    for (var ind = 0; ind < option['yAxis'].length; ind++) {
      if (option['yAxis'][ind]['axisLabel']['formatter_func']) {
        var f = new Function(option['yAxis'][ind]['axisLabel']['formatter_func'].arguments,
                             option['yAxis'][ind]['axisLabel']['formatter_func'].body)
        option['yAxis'][ind]['axisLabel']['formatter'] = f
      }
    }
  }
  else {
    if (option['yAxis']['axisLabel']['formatter_func']) {
      var f = new Function(option['yAxis']['axisLabel']['formatter_func'].arguments,
                           option['yAxis']['axisLabel']['formatter_func'].body)
      option['yAxis']['axisLabel']['formatter'] = f
    }
  }
  return option;
}

function custom_tooltip(option, dimension=2) {

  if (dimension === 2) {
    var xaxis_key = 'xAxis'
    var yaxis_key = 'yAxis'
  }

  else if (dimension === 3) {
    var xaxis_key = 'xAxis3D'
    var yaxis_key = 'yAxis3D'
    var zaxis_key = 'zAxis3D'
  }

  if (option['radar']) {
    var radar_names = []
    for (var ind_ = 0; ind_ < option['radar']['indicator'].length; ind_++) {
      radar_names.push(option['radar']['indicator'][ind_]['name']) 
    }
  }
  
  
  if (option[xaxis_key]['name'] !== null && option[xaxis_key]['name'] !== '' && Array.isArray(option[xaxis_key])!==true) {
    var xaxis_name = option[xaxis_key]['name'];
  }
  else {
    var xaxis_name = 'X';
  }

  if (option[yaxis_key]['name'] !== null && option[yaxis_key]['name'] !== ''&& Array.isArray(option[xaxis_key])!==true) {
    var yaxis_name = option[yaxis_key]['name'];
  }
  else {
    var yaxis_name = 'Y';
  }

  if (typeof zaxis_key !== 'undefined') {
    if (option[zaxis_key]['name'] !== ''&& Array.isArray(option[xaxis_key])!==true) {
      var zaxis_name = option[zaxis_key]['name'];
    }
    else {
      var zaxis_name = 'Z';
    }
  }
  
  if (option['tooltip']) {
    if (option['tooltip']['precision']) {
      var precision = option['tooltip']['precision']
      option['tooltip']['valueFormatter'] = (value) =>  Math.round(Number(value) * (10**precision)) / (10**precision)
    }

    for (var ind_ = 0; ind_ < option['series'].length; ind_++) {
      if (option['series'][ind_]['tooltip']) {
        if (option['series'][ind_]['tooltip']['precision']) {
          var precision = option['series'][ind_]['tooltip']['precision']
          const fix = precision_ => value => Math.round(Number(value) * (10**precision_)) / (10**precision_),
          fix_p = fix(precision);
          option['series'][ind_]['tooltip']['valueFormatter'] = function (value) {
            return fix_p(value)
          } 
        }
      }
    }

    if (option['series'].length === 1) {
      if (['scatter', 'heatmap', 'scatter3D', 'radar'].includes(option['series'][0]['type'])) {
        option['tooltip']['formatter'] = function(params) {
          if (params.seriesName.includes('series')) {
            var series_name = ''
          }
          
          else {
            var series_name = params.seriesName + '<br>'
          }
      
          if (params.seriesType === 'scatter') {
            formatter = series_name
                + xaxis_name + ': '+ Math.round(params.value[0] * 100) / 100
                +'<br>' + yaxis_name + ': ' + Math.round(params.value[1] * 100) / 100
          }
  
          else if (params.seriesType === 'heatmap') {
            formatter = params.name + ', ' + option['yAxis'][0]['data'][params.data[1]] + '<br> <b>' + Math.round(params.data[2] * 10000) / 10000
          }
      
          else if (params.seriesType === 'scatter3D') {
            formatter = series_name
                + xaxis_name + ': '+ Math.round(params.value[0] * 100) / 100
                +'<br>' + yaxis_name + ': ' + Math.round(params.value[1] * 100) / 100
                +'<br>' + zaxis_name + ': ' + Math.round(params.value[2] * 100) / 100
          }
          
          else if (params.seriesType === 'radar') {
            formatter = params.name  + '<br>';
            for (var ind_ = 0; ind_ < option['radar']['indicator'].length; ind_++) {
              if (ind_ !== option['radar']['indicator'].length - 1) {
                formatter += radar_names[ind_] + ': ' + Math.round(params.value[ind_] * 100) / 100 + '<br>'
              }
              else {
                formatter += radar_names[ind_] + ': ' + Math.round(params.value[ind_] * 100) / 100
              }
            }
          }
        return formatter;
        }
      }
    }
    else {
      for (var out_ind_ = 0; out_ind_ < option['series'].length; out_ind_++) {
        if (['scatter', 'heatmap', 'scatter3D', 'radar'].includes(option['series'][out_ind_]['type'])) {
          if (option['series'][out_ind_]['tooltip']) {
          }
          else {
            option['series'][out_ind_]['tooltip'] = {}
          }
          option['series'][out_ind_]['tooltip']['formatter'] = function(params) {
            if (params.seriesName.includes('series')) {
              var series_name = ''
            }
            
            else {
              var series_name = params.seriesName + '<br>'
            }
        
            if (params.seriesType === 'scatter') {
              formatter = series_name
                  + xaxis_name + ': '+ Math.round(params.value[0] * 100) / 100
                  +'<br>' + yaxis_name + ': ' + Math.round(params.value[1] * 100) / 100
            }
    
            else if (params.seriesType === 'heatmap') {
              if ('data' in option['yAxis'][option['series'][params.seriesIndex]['yAxisIndex']]) {
                formatter = params.name + ', ' + option['yAxis'][option['series'][params.seriesIndex]['yAxisIndex']]['data'][params.data[1]] + '<br> <b>' + Math.round(params.data[2] * 10000) / 10000
              }
              else {
                formatter = Math.round(params.data[2] * 10000) / 10000
              }
                
            }
        
            else if (params.seriesType === 'scatter3D') {
              formatter = series_name
                  + xaxis_name + ': '+ Math.round(params.value[0] * 100) / 100
                  +'<br>' + yaxis_name + ': ' + Math.round(params.value[1] * 100) / 100
                  +'<br>' + zaxis_name + ': ' + Math.round(params.value[2] * 100) / 100
            }
            
            else if (params.seriesType === 'radar') {
              formatter = params.name  + '<br>';
              for (var ind_ = 0; ind_ < option['radar']['indicator'].length; ind_++) {
                if (ind_ !== option['radar']['indicator'].length - 1) {
                  formatter += radar_names[ind_] + ': ' + Math.round(params.value[ind_] * 100) / 100 + '<br>'
                }
                else {
                  formatter += radar_names[ind_] + ': ' + Math.round(params.value[ind_] * 100) / 100
                }
              }
            }
          return formatter;
          }
        }
      }
    }
  }
  return option;
};

function support_brush_event(option) {
  if (option['event']['type_'] === 'brushselected') {
    if (option['link_id'] === null) {
      var link_id = option['chart_id'];
    }
    else {
      var link_id = option['link_id'];
    }
    var dom = document.getElementById(link_id);
    var bind_chart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });
    var last_selected = [];
    bind_chart.on(option['event']['type_'], (params) => {
      var brushed = [];
      var brushComponent = params.batch[0];
      for (var sIdx = 0; sIdx < brushComponent.selected.length; sIdx++) {
        var rawIndices = brushComponent.selected[sIdx].dataIndex;
        brushed.push(rawIndices);
      }
      var brushed_all = brushed[0];

      if (JSON.stringify(last_selected) !== JSON.stringify(brushed_all)) {

        // Update memory
        let testRequest = new Request('http://localhost:' + option['port'] +'/function/js_call_python_function', {
          method: 'post',
          headers: {
              'Content-Type': 'application/json;charset=utf-8;',
              'Access-Control-Allow-Origin':'*',
              'Access-Control-Allow-Credentials': 'true',
              'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
          },
          body: JSON.stringify({'js_func_input':{'selected': brushed_all},
                                'event_id': option['event']['event_id']})
        });
        var dom_dict = {}
        fetch(testRequest).then(response => {
          var result = response.json();
          result.then(res => {
            dom_dict[res['link_id']] = document.getElementById(res['link_id']);
            setInnerHTML(dom_dict[res['link_id']], res['html']);
          });
        });
        last_selected = brushed_all;
      }
                            
    // bind_chart.setOption(option);
    })
  }
  return option;
};

function support_click_event(option) {
  if (option['event']['type_'] === 'click') {
    if (option['link_id'] === null) {
      var link_id = option['chart_id'];
    }
    else {
      var link_id = option['link_id'];
    }
    var dom = document.getElementById(link_id);
    var bind_chart = echarts.init(dom, null, {
        renderer: 'canvas',
        useDirtyRect: false
    });

    if (option['series'][0]['orient'] === 'vertical') {
      var value_idx = 0
    }
    else {
      var value_idx = 1
    }
    

    bind_chart.on(option['event']['type_'], (params) => {
      if (option['event']['task'] === 'singleselect') {
        for (var ind_2 = 0; ind_2 < option['series'][0]['data'].length; ind_2++) {
          if (option['series'][0]['data'][ind_2]['itemStyle']['color'] !== '#1f77b4') {
            option['series'][0]['data'][ind_2]['itemStyle']['color'] = '#1f77b4';
          }
        }
        var idx = option['series'][0]['x_value'].indexOf(params.value[value_idx])
        option['series'][0]['data'][idx]['itemStyle']['color'] = '#ff7f0e';

        var selected = params.value[value_idx];
      }
      else {
        console.log(params);
      }
      
      let testRequest = new Request('http://localhost:' + option['port'] +'/function/js_call_python_function', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json;charset=utf-8;',
          'Access-Control-Allow-Origin':'*',
          'Access-Control-Allow-Credentials': 'true',
          'Access-Control-Allow-Methods':'POST,PATCH,OPTIONS'
        },
        body: JSON.stringify({'js_func_input':{'selected': selected},
                              'event_id': option['event']['event_id']})
      });
      var dom_dict = {}
      fetch(testRequest).then(response => {
        var result = response.json();
        result.then(res => {
          dom_dict[res['link_id']] = document.getElementById(res['link_id']);
          setInnerHTML(dom_dict[res['link_id']], res['html']);
        });
      });
      bind_chart.setOption(option);
    });
  }
  return option;
};