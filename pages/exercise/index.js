// pages/exercise/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl
import getCalendar from "../../components/calendar/calendar"
Page({

  /**
   * 页面的初始数据
   */
  data: {
    taskId:0,
    userId:'',
    list: [],
    ddl:'',
    name:'',
    diff:null,
    diffs:['易','中','难'],
    done:'',
    all:'',
    detail:'',
    results:[
      {
        date:'04-16',
        isMorn:1,
        time:'10:00',
        grades:95,
        advice:'本次的练习中，请注意手臂抬起的角度与高度。其中，右臂与右肩的角度可以适当减小，避免过度训练，引起右大臂肌肉群拉伤，影响右大臂肌肉功能恢复。'
      },
      {
        date:'04-15',
        isMorn:0,
        time:'14:00',
        grades:89,
        advice:'在摆臂练习中，要注意手臂抬起的角度与高度。注意不要过度训练，引起肌肉损伤。'
      },
    ],
    
   
  },
  goTo:function(){
    wx.navigateTo({
      url: '../video/index',
    })
  },
  // 获取用户信息
  getInfo:function(){
    const that=this
    wx.getStorage({
      key: 'userInfo',
      success (res) {
        //console.log(res)
        that.setData({
          userId:res.data.userId,
        });
      },
    })
    wx.getStorage({
      key: 'taskInfo',
      success (res) {
        //console.log(res)
        that.setData({
          taskId:res.data.taskId,
        });
      },
    })
  },

  // 获取任务训练结果
  getResult:function(page){
    //console.log(page.data)
    wx.request({
      url: baseUrl+'/detail/get',
      method:'POST',
      data:{
        task:page.data.taskId,
      },
      success:(res)=>{
        //console.log(res)
        page.setData({
          results:res.data
        })
      }
    })
  },

  //获取任务详情
  getDetail:function(page){
    //console.log(page.data)
    wx.request({
      url: baseUrl+'/task/get_info',
      method:'POST',
      data:{
        id:page.data.taskId,
      },
      success:(res)=>{
        //console.log(res);
        page.setData({
          ddl:res.data.ddl,
          name:res.data.name,
          diff:res.data.diff,
          done:res.data.done,
          all:res.data.all,
          detail:res.data.detail,
        })
      }
    })
  },

  /**
   * 获取日历信息
   */
  getCalender:function(page){
    //console.log(page.data)
    let aa=page.selectComponent("#calendar")
    wx.request({
      url: baseUrl+'/task/date_list',
      method:'POST',
      data:{
        id:page.data.taskId
      },
      success(res){
        // console.log("this")
        // console.log(res)
        page.setData({
          list:res.data
        })
        aa.getCalendar()
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //console.log(options)
    this.getInfo()
    let myPage=this
    setTimeout(function(){myPage.getDetail(myPage);},100)
    setTimeout(function(){myPage.getResult(myPage);},100)
    setTimeout(function(){myPage.getCalender(myPage);},100)

    
    
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