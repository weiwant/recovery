// pages/video/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl

wx.cloud.init({
  env:'recovery-1gpfqg1b2321ce8b',
})

Page({
  
  /**
   * 页面的初始数据
   */
  data: {
    taskId:null,
    src: '',        //上传视频临时地址
    video:'',       //视频地址
  },

  // 获取用户信息
  getInfo:function(){
    const that=this
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

  // 删除视频
  deleteVideo(e) {
    wx.showModal({
      title: '删除视频',
      content: '确定要删除这段视频吗？',
      cancelText: '再看看',
      confirmText: '是的',
      success: res => {
          this.setData({
            src: ''
          })
        }
      })
  },

  

  // 选取视频
  chooseV:function(){
    let mypage=this
    wx.chooseVideo({
      success (res) {
        const tempFilePaths = res.tempFilePath
        console.log(tempFilePaths);
        mypage.setData({
          src: res.tempFilePath,
        })
      }
    })
  },
  
  // 上传视频并跳转至结果页面
  goToResult:function(){
    let mypage=this
    console.log(mypage.data)
    wx.showLoading({
      title: '上传中',
    })
    wx.uploadFile({
      url: baseUrl+'/detail/upload', 
      filePath: mypage.data.src,
      name: 'video',
      formData: {
        'task':mypage.data.taskId,
        'video_type':'mp4',
      },
      success (res){
        wx.hideLoading()
        const data = res.data
        console.log(res)
        mypage.setData({
          video:data
        })
        wx.navigateTo({
          url: '../results/index?video='+mypage.data.video,
        })
      },
      fail (res){
        console.log(res);
        wx.showToast({
          title: '上传失败',
          icon: 'error',
        })
      }
    })

    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.getInfo()
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