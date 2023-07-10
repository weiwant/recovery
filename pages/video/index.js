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
    src: '',        // 上传视频临时地址
    fileID:[],      //视频在云存储里的id
    video:'',       //视频https地址
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
  chooseVideo: function() {
    var _this = this;
    wx.chooseVideo({
      success: function(res) {
        _this.setData({
          src: res.tempFilePath,
        })
        _this.uploadvideo()
      }
    })
  },

  /**
   * 上传视频至云服务器 目前后台限制最大100M, 以后如果视频太大可以选择视频的时候进行压缩
   */
  uploadvideo(){
    var src = this.data.src;
    wx.cloud.uploadFile({
      cloudPath: String(Date.parse(new Date()))+'训练视频.mp4', // 上传至云端的路径
      filePath: src, // 小程序临时文件路径
      success: res => {
        // 返回文件 ID
        console.log(res.fileID)
        this.data.fileID.push(res.fileID)
        this.test()
      },
      fail: console.error
    })
  },

  //转https
  test(){
    console.log(this.data);
    const httpsLinks =  this.batchFileIdToHttps(this.data.fileID, 'FTH');
    this.setData({
      video:httpsLinks[0]
    })
    console.log(this.data)
  } ,


  /**
 * 根据fileID获取HTTPS链接
 * @param {Array} fileID 需要转换的fileID数组
 * @param {String} type 转化类型（默认FTH），可选值：FTH（FileIdToHttps：fileID转https）、GTU（getTempFileURL：用fileID获取临时https地址）
 * @param {String} env 环境id（当type=GTU时才需要填写，若所需环境为默认环境则无需填写）
 * @param {String} appid 环境所属appid（若传env，则appid必传）
 * @return {Array} 返回HTTPS链接
 */
  batchFileIdToHttps(fileIds,type='FTH',env,appid) {
  if(!Array.isArray(fileIds)){
    throw new Error('数据类型必须是数组')
  }
  if(type == 'FTH') return FTH(fileIds);
  else if(type == 'GTU') return GTU(fileIds,env,appid);
  else throw new Error('type参数不正确')
 
  function FTH(fileIds) {
    console.log('fileID转https');
    return fileIds.map(fileId => {
      const regex = /cloud:\/\/(.+)\.([^\/]+)\/(.+)/;
      const match = fileId.match(regex);
      if (!match) {
        return '无法兑换成https链接';
      }
      // const envId = match[1];
      const customId = match[2];
      const path = match[3];
      return `https://${customId}.tcb.qcloud.la/${path}`;
    });
  }
 
  async function GTU(fileIds,env,appid) {
    console.log('用fileID获取临时https地址');
    // 声明新的 cloud 实例
    const cloud = env && appid ? new wx.cloud.Cloud({
      // 资源方 AppID
      resourceAppid: appid,
      // 资源方环境 ID
      resourceEnv: env,
    }) : wx.cloud
    await cloud.init();
    const promise = new Promise((resolve, reject) => {
      cloud.getTempFileURL({
        fileList: fileIds,
        config: {
          env: env ? env : ''
        },
        success: res => {
          const fileList = [];
          for (const item of res.fileList) {
            fileList.push(item.tempFileURL)
          }
          resolve(fileList);
        },
        fail: err => {
          const fileList = [];
          for (const item of fileIds) {
            fileList.push('获取临时地址失败')
          }
          reject(fileList);
        }
      })
    });
    return promise;
  }
  },

  upload: function() {
    console.log(this.data)
    wx.request({
      url: baseUrl+'/detail/upload',
      method:'POST',
      data:{
        task:this.data.taskId,
        video:this.data.video,
      },
      success:(res)=>{
        wx.navigateTo({
          url: '../results/index',
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