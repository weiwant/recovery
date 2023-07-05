// pages/userInfo/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    index:0,
    picker: ['患者', '医生'],
    sexIndex:0,
    sexPicker:['男','女'],
    userImg:' ',
    nickName:'细品岁月',
    modalName:'',
    realName:'请输入您的真实姓名',
  },
  PickerChange(e) {
    console.log(e);
    this.setData({
      index: e.detail.value
    })
  },
  SexPickerChange(e){
    console.log(e);
    this.setData({
      sexIndex: e.detail.value
    })
  },
  ChooseImage() {
    wx.chooseImage({
      count: 1, //默认9
      sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album'], //从相册选择
      success: (res) => {
          this.setData({
            userImg: res.tempFilePaths
          })
      }
    });
  },
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  getNewNickname:function(e){
    const that = this;
    that.setData({
      nickName:e.detail.value.nickname,
    })
  },
  getNewName:function(e){
    const that = this;
    that.setData({
      realName:e.detail.value.name,
    })
  },

  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
 
  confirm(e){
    wx.setStorage({
      key:"userInfo",
      data:{
        nickname:this.data.nickName,
        userImg:this.data.userImg,
      }
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {
    var that = this;
    // 从用户缓存中获取数据
    wx.getStorage({
      key: 'userInfo',
      success (res) {
        console.log(res.data);
        that.setData({
          nickName:res.data.nickname,
          userImg:res.data.userImg,
          userId:'203254455'
        });
      },
    })
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