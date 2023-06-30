// pages/circleDetail/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    postId:0,
    index:0,
    iconName:['cuIcon-appreciatefill','cuIcon-appreciate'],
    tt:['已赞(884)','点赞(883)'],
    userImg:'https://s2.loli.net/2023/04/14/boRaWVHMzskLc6B.jpg',
    userName:'疗康院康复师9527',
    isDoctor:1,
    time:'2023年4月3日 14:44',
    content:'&emsp;&emsp;今天很荣幸参加了由GZCPT主办的脑卒中康复治疗学习班，“镜”观其变，以“镜”促动--带您走进脑卒中后康复的镜像世界了解到了新镜子疗法。在这里把一些要点分享给大家。\n&emsp;&emsp;镜像疗法是基于镜像神经元理论，利用大脑的可塑性,通过视觉反馈、运动观察、运动想象、运动模仿来进行康复训练的一种治疗手段。根据镜面反射相等的物象,以正常肢体镜像代替患侧肢体。患者通过这样视觉反馈进行运动观察，模仿以及再学习。',
    view:1684,
    isGood:0,
    good:883,
    comment:307,
    imgList:[
      {url:'https://s2.loli.net/2023/04/14/nMYUPyKBTxjgqSG.png'},
      {url:'https://s2.loli.net/2023/04/14/VkqXaetJ3cGCnAU.png'},
      {url:'https://s2.loli.net/2023/04/14/ksPzQiIdbVg5rZm.png'},
    ],
    commentList:[
      {
        userUrl:'https://s2.loli.net/2023/04/26/NZctY6iLEuHvpAI.jpg',
        userName:'喜洋洋',
        content:'从我的个人经验来说 我认为这个训练是有用的。。',
        time:'2023年4月5日 08:21',
        isGood:1,
        children:[
          {
            username:'疗康院康复师9527',
            cont:'贵在坚持，会有效果的！✊'
          },
          {
            username:'咪宝的阿婆',
            cont:'：训练了多久哇'
          }
        ]
      },
      {
        userUrl:'https://s2.loli.net/2023/04/26/SVwHirl9U63aQyz.jpg',
        userName:'心渡',
        content:'真的有用吗？可以再说详细一点吗？',
        time:'2023年4月4日 18:17',
        isGood:0,
        children:[
          {
            username:'疗康院康复师9527',
            cont:'：可以看我的最新博文🙂'
          },
        ]
      },
    ]
  },
  change:function(){
    this.setData({
      index: (this.data.index + 1) % 2
    })
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
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      postId: options.id,
    });
    //console.log(this.data.postId);
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