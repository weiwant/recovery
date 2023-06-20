// custom-tab-bar/index.js
Component({
	properties: {},
	data: {
        //当前高亮项
		selected: 0,
        //tabBar页面数据
		tabList: [
          {
            "pagePath": "pages/index/index",
            "text": "康复"
          },
          {
            "pagePath": "pages/news/index",
            "text": "科普"
          },
          {
            "pagePath": "pages/circle/index",
            "text": "交流"
          },
          {
            "pagePath": "pages/mine/index",
            "text": "我的"
          }
		]
	},
	attached: function() {},
	methods: {
		//底部切换
		switchTab(e) {
			let key = Number(e.currentTarget.dataset.index);
			let tabList = this.data.tabList;
			let selected= this.data.selected;
			
			if(selected !== key){
				this.setData({
					selected:key
				});
				wx.switchTab({
					url: `/${tabList[key].pagePath}`,
				})
			}
		},
  },
  tabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
		this.getTabBar().setData({
			selected: 0
	  	})
  	}
  }
})
