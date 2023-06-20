// index.js
// 获取应用实例
import * as echarts from '../../ec-canvas/echarts';

const app = getApp();

function initChart(canvas, width, height, dpr) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height,
    devicePixelRatio: dpr // new
  });
  canvas.setChart(chart);

  var option = {
    title: {
      text: '近一周训练结果',
      left: 'center'
    },
    legend: {
      data: ['抬臂练习', '抬腿练习'],
      top: 30,
      left: 'center',
      z: 100
    },
    grid: {
      containLabel: true
    },
    tooltip: {
      show: true,
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['4.12', '4.13', '4.14', '4.15', '4.16', '4.17', '4.18'],
      // show: false
    },
    yAxis: {
      x: 'center',
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
      // show: false
    },
    series: [{
      name: '抬臂练习',
      type: 'line',
      smooth: true,
      data: [2,3, 3, 4, 4, 5, 3]
    }, {
      name: '抬腿练习',
      type: 'line',
      smooth: true,
      data: [5, 5, 4, 5, 3, 4, 5]
    }]
  };

  chart.setOption(option);
  return chart;
}

Page({
  data: {
    ec: {
      onInit: initChart
    },
    colors:['bg-red','bg-blue'],
    btn:['去接受','去打卡'],
    index:0,
  },

  onReady() {
  },
  onShow(){
    this.tabBar();
  },
  
  tabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 0
      })
    }
  },
  goTo:function(){
    wx.navigateTo({
      url: '../exercise/index',
    })
  },
  change:function(){
    this.setData({
      index: (this.data.index + 1) % 2
    })
  }
});

