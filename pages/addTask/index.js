// pages/addTask/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl
//recovery/api/task/add

import {dateFormat} from '../../utils/dateformat/dateformat'

Page({

  /**
   * 页面的初始数据
   */
  data: {
    pIndex: null,
    patients: [
      {
        name:'李淑芬',
        patientId:'lsfjds525'
      },
      {
        name:'李强',
        patientId:'lqus3522dhs'
      }
    ],
    dIndex:null,
    difficulty:['易','中','难'],
    selectedDif:0,
    date:null,
    doctorId:'zzp1568789965',
    //当前选择用户
    selectedPatient:'',
    circle_time:'',
    type:'',
    description:''
  },
  /**
   * 添加task
   * 
   */
  addTask(){
    
    wx.request({
      url: baseUrl+'/task/add',
      method:'POST',
      data:{
        doctor:this.data.doctorId,
        patient:this.data.selectedPatient,
        description:this.data.description,
        deadline:dateFormat(this.data.date).format('YYYY-MM-DD'),
        circle_time:this.data.circle_time,
        type:this.data.type,
        difficulty:this.data.selectedDif
      },
      success:(res)=>{
        wx.showToast({
          title: '发布成功',
        })
      }
    })
  },
  DateChange(e) {
    var nn=new Date(this.data.date)
    //nn=dateFormat(nn).format('YYYY-MM-DD')
    nn=dateFormat(this.data.date).format('YYYY-MM-DD')
    
    console.log(nn)

    this.setData({
      date: e.detail.value
    })
  },
  /**
   * 患者选择
   */
  PickerChange(e) {
    //console.log(e);
    this.setData({
      pIndex: e.detail.value,
      selectedPatient:this.data.patients[e.detail.value].patientId
    })
    //console.log(this.data.patients[e.detail.value].patientId)
  },
  /**
   * 难度选择
   */
  PickerChange1(e) {
    //console.log(e);
    this.setData({
      dIndex: e.detail.value,
      selectedDif:e.detail.value
    })
  },
  /**
   * 医生获取与自己绑定的患者，用于发布任务时选择患者
   */
  getMyPatient(){

    //this.setdata({
    //  patients:res.data  
    //})

  },
  /**
   * 周期输入监听
   */
  circleinput(e){
    //console.log(e)
    this.setData({
      circle_time:e.detail.value
    })
  },
  /**
   * 任务type输入监听
   */
  typeinput(e){
    this.setData({
      type:e.detail.value
    })
  },
  /**
   * 任务详情监听
   */
  describeinput(e){
    this.setData({
      description:e.detail.value
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //从缓存读医生id
    // this.setData({
    //   doctorId:
      
    // })

    //获取当前日期
    var today=dateFormat(new Date()).format('YYYY-MM-DD')
    //console.log(month)
    this.setData({
      date:today
      
    })
    
    

    //获取医生对应患者列表
    this.getMyPatient()

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})