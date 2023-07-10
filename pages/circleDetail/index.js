// pages/circleDetail/index.js
const app=getApp()
const baseUrl=app.globalData.baseUrl

Page({

  /**
   * 页面的初始数据
   */
  data: {
    postId:'',
    userId:'lsfjds525',
    detail:[],
    isGood:0,
    
    //评论内容
    comment:'',
    parent:null,
    
    
  },
  /**
   * 获取帖子详情
   */
  getPostDetail(){
    wx.request({
      url: baseUrl+'/posts/get_detail',
      method:'POST',
      data:{
        //以后从缓存读吧
        userid:this.data.userId,
        id:this.data.postId
      },
      success:(res)=>{
        //console.log(res.data)
        this.setData({
          detail:res.data
        })
        
      }
    })

  },
  /**
   * 点赞
   */
  change:function(e){
    console.log(e)
    //点赞数
    var stars="detail.stars"
    //传递后端
    if(1!=this.data.isGood){
      //点赞
      this.setData({
        isGood:1,
        //点赞数
        [stars]:this.data.detail.stars+1
      })
      wx.request({
        url: baseUrl+'/posts/like',
        method:'POST',
        data:{
          userid:this.data.userId,
          post_id:this.data.postId
          
        },
        success:(res)=>{
          console.log(res)
        }
      })
    } else {
      //取消点赞
      this.setData({
        isGood:0,
        //点赞数
        [stars]:this.data.detail.stars-1
      })
      wx.request({
        url: baseUrl+'/posts/dislike',
        method:'POST',
        data:{
          userid:this.data.userId,
          post_id:this.data.postId
          
        },
        success:(res)=>{
          console.log(res)
        }
      })
    }
  },
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
  /**
   * 输入框内容获取
   */
  commentInput(e){
    //console.log(e)
    this.setData({
      comment:e.detail.value
    })
  },
  /**
   * 普通评论
   */
  say(){
    wx.request({
      url: baseUrl+'/posts/comment',
      method:'POST',
      data:{
        commenter:this.data.userId,
        post_id:this.data.postId,
        parent:this.data.parent,
        content:this.data.comment

      },
      success:(res)=>{
        console.log(res)
        wx.showToast({
          title: '评论成功',
        })
        this.setData({
          comment:''
        })
        this.onShow()
      }
    })
    
  },
  /**
   * 子评论
   */
  sonSay(e){
    //获取父评论id
    console.log(e)
    var fComment=e.currentTarget.dataset.commentid
    this.setData({
      parent:fComment
    })
    this.say()
    this.setData({
      parent:null
    })

  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //console.log(options)
    this.setData({
      postId:options.id,
      isGood:options.isgood
    });
    this.getPostDetail()
    
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
    this.getPostDetail()
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