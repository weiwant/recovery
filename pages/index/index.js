// index.js
// 获取应用实例
import * as echarts from '../../ec-canvas/echarts';

const app = getApp();
const baseUrl=app.globalData.baseUrl

/**
 * 任务完成图表
 */
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
    //1患者，0医生
    isPatient:1,
    doctorId:'255455mo',
    patientId:'lsfjds525',
    colors:['bg-red','bg-blue','bg-green'],
    btn:['去接受','去打卡','已完成'],
    diff:['易','中','难'],
    index:0,
    activeNames: ['1'],
    taskList:[
      // {
      //   taskId:1,
      //   url:'https://s2.loli.net/2023/04/17/mbhk3zOcYalJE1Q.jpg',
      //   doctor:'赵医生',
      //   time:'2023年4月10日 9:31',
      //   ddl:'2023年5月5日',
      //   name:'步行练习',
      //   diff:'难',
      //   done:0,
      //   all:'30天',
      //   status:0,
      //   detail:'',
      // },
      // {
      //   taskId:2,
      //   url:'https://s2.loli.net/2023/04/17/mbhk3zOcYalJE1Q.jpg',
      //   doctor:'赵医生',
      //   time:'2023年4月1日 14:24',
      //   ddl:'2023年4月28日',
      //   name:'抬臂练习',
      //   diff:'中',
      //   done:11,
      //   all:'20天',
      //   status:1,
      //   detail:'',
      // },
      // {
      //   taskId:3,
      //   url:'https://s2.loli.net/2023/04/17/mbhk3zOcYalJE1Q.jpg',
      //   doctor:'赵医生',
      //   time:'2023年3月3日 10:47',
      //   ddl:'2023年4月6日',
      //   name:'抬腿练习',
      //   diff:'易',
      //   done:30,
      //   all:'30天',
      //   status:2,
      //   detail:'',
      // }
    ],
    patientList:[
      // {
      //   id:1,
      //   patientImg:'https://s2.loli.net/2023/04/14/vZo9rCgjNGIPSb2.jpg',
      //   patientName:'李淑芬',
      //   patientId:'2789257855',
      //   taskList:[
      //     {taskName:'抬臂练习',},
      //     {taskName:'抬腿练习',},
      //     {taskName:'步行练习',},
      //   ]
      // },
      // {
      //   id:2,
      //   patientImg:'https://s2.loli.net/2023/04/18/AQGDHMYIja9Nd2g.jpg',
      //   patientName:'赵书',
      //   patientId:'2032578554',
      //   taskList:[
      //     {taskName:'抬臂练习',},
      //     {taskName:'抬腿练习',},
      //     {taskName:'步行练习',},
      //   ]
      // },
      // {
      //   id:3,
      //   patientImg:'https://s2.loli.net/2023/04/14/SfTo1UYsOCZwBM2.jpg',
      //   patientName:'王国发',
      //   patientId:'2357846781',
      //   taskList:[
      //     {taskName:'抬臂练习',},
      //     {taskName:'抬腿练习',},
      //     {taskName:'步行练习',},
      //   ]
      // },
    ]
  },
  // 医生获取患者列表
  getPatientList:function(){
    wx.request({
      url: baseUrl+'/user/get_task_doctor',
      method:'POST',
      data:{
        doctor:this.data.doctorId

      },
      success:(res)=>{
        console.log(res),
        this.setData({
          patientList:res.data
        })
      }
    })
  },
  // 患者获取任务列表
  getTaskList:function(){
    wx.request({
      url: baseUrl+'/task/get',
      method:'POST',
      data:{
        patient:this.data.patientId
      },
      success:(res)=>{
        console.log(res),
        this.setData({
          taskList:res.data
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //获取当前医生id
    if(!this.data.isPatient){
      //医生获取患者任务列表
      this.getPatientList()
    }
    // 患者获取康复任务列表
    else{
      this.getTaskList()
    }
    


  },
  /**
   * 
   */
  onReady() {

  },
  onShow(){
    this.tabBar();
    if(!this.data.isPatient){
      //医生获取患者任务列表
      this.getPatientList()
    }
    // 患者获取康复任务列表
    else{
      this.getTaskList()
    }
  },
  
  tabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 0
      })
    }
  },
  
  onChange(event) {
    this.setData({
      activeNames: event.detail,
    });
  },

  goToExercise:function(e){
    wx.setStorage({
      key:"taskInfo",
      data:{
        taskId:e.currentTarget.dataset.id,
      }
    });
    wx.navigateTo({
      url: '../exercise/index?',
    })
  },

  goToAdd:function(){
    wx.navigateTo({
      url: '../addTask/index',
    })
  },

  change:function(){
    this.setData({
      index: (this.data.index + 1) % 2
    })
  }
});

