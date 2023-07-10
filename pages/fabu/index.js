// pages/fabu/index.js
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
    nickName:'李淑芬',
    userId:'',
    content:'',
    imgList: [],
    imgs:[],
    links:[],
  },

  // 从相册里选取图片
  ChooseImage() {
    wx.chooseImage({
      count: 9, //默认9
      sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album'], //从相册选择
      success: (res) => {
        console.log(res.tempFilePaths[0]);
        if (this.data.imgList.length != 0) {
          this.setData({
            imgList: this.data.imgList.concat(res.tempFilePaths)
          })
          this.uploadImg(res.tempFilePaths[0],this.data.imgList.length)
        } else {
          this.setData({
            imgList: res.tempFilePaths
          })
          this.uploadImg(res.tempFilePaths[0],this.data.imgList.length)
        }
      }
    });
  },

  // 将图片上传至云存储
  uploadImg(str,i){
    wx.cloud.uploadFile({
      cloudPath: String(Date.parse(new Date()))+String(i)+'.png', // 上传至云端的路径
      filePath: str, // 小程序临时文件路径
      success: res => {
        // 返回文件 ID
        console.log(res.fileID)
        this.data.imgs.push(res.fileID)
      },
      fail: console.error
    })
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

  // 向数据库传输数据
  post(page){
    wx.request({
      url: baseUrl+'/posts/add',
      method:'POST',
      data:{
        creator:page.data.userId,
        content:page.data.content,
        pictures:page.data.links,
      },
      success:(res)=>{
        //console.log(res)
        wx.showToast({
          title: '发布成功',
        })
      }
    })
  },

// 发布帖子
  publish(){
    let myPage = this
    console.log(this.data)
    this.test()
    setTimeout(function(){myPage.post(myPage);},1000)
  },
  //转https
   test(){
    const httpsLinks =  this.batchFileIdToHttps(this.data.imgs, 'FTH');
    this.setData({
      links:httpsLinks
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