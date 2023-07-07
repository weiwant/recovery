// pages/fabu/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl

Page({

  /**
   * 页面的初始数据
   */
  data: {
    nickName:'李淑芬',
    userId:'',
    content:'',
    imgList: [],
  },

  // 从相册里选取图片
  ChooseImage() {
    wx.chooseImage({
      count: 9, //默认9
      sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album'], //从相册选择
      success: (res) => {
        if (this.data.imgList.length != 0) {
          this.setData({
            imgList: this.data.imgList.concat(res.tempFilePaths)
          })
        } else {
          this.setData({
            imgList: res.tempFilePaths
          })
        }
      }
    });
  },

  // 查看所选图片
  ViewImage(e) {
    wx.previewImage({
      urls: this.data.imgList,
      current: e.currentTarget.dataset.url
    });
  },

  //删除所选图片
  DelImg(e) {
    wx.showModal({
      title: '删除图片',
      content: '确定要删除这张图片吗？',
      cancelText: '再看看',
      confirmText: '是的',
      success: res => {
        if (res.confirm) {
          this.data.imgList.splice(e.currentTarget.dataset.index, 1);
          this.setData({
            imgList: this.data.imgList
          })
        }
      }
    })
  },

// 从用户缓存中获取数据
  getInfo:function(){
    var that = this;
    wx.getStorage({
      key: 'userInfo',
      success (res) {
        console.log(res.data);
        that.setData({
          userId:res.data.userId,
          nickName:res.data.nickname,
        });
      },
    })
  },

// content内容监听
  contentInput(e){
    //console.log(e.detail.value)
    this.setData({
      content:e.detail.value
    })
  },

// 发布帖子
  publish(){
    console.log(this.data)
    wx.request({
      url: baseUrl+'/posts/add',
      method:'POST',
      data:{
        creator:this.data.userId,
        content:this.data.content,
        pictures:this.data.imgList,
      },
      success:(res)=>{
        //console.log(res)
        wx.showToast({
          title: '发布成功',
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.getInfo();
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