var data_hb_mai =
{
    items:
    [
      { key:0,rate:10000 },
      { key:1,rate:10000 },
      { key:2,rate:9000 },
      { key:3,rate:8000 },
      { key:4,rate:7000 },
      { key:5,rate:6000 },
      { key:6,rate:5000 },
      { key:7,rate:4000 },
      { key:8,rate:3000 },
      { key:9,rate:2000 },
      { key:10,rate:1000 },
      { key:11,rate:0 },
      { key:12,rate:0 },
      { key:13,rate:0 },
      { key:14,rate:0 },
      { key:15,rate:0 },
      { key:16,rate:0 },
      { key:17,rate:0 },
      { key:18,rate:0 },
      { key:19,rate:0 },
      { key:20,rate:0 },
      { key:21,rate:0 },
      { key:22,rate:0 },
      { key:23,rate:0 },
      { key:24,rate:0 },
      { key:25,rate:0 },
      { key:26,rate:0 },
      { key:27,rate:0 },
      { key:28,rate:0 },
      { key:29,rate:0 },
      { key:30,rate:0 },
      { key:31,rate:0 },
      { key:32,rate:0 },
      { key:33,rate:0 },
      { key:34,rate:0 },
      { key:35,rate:0 },
      { key:36,rate:0 },
      { key:37,rate:0 },
      { key:38,rate:0 },
      { key:39,rate:0 },
      { key:40,rate:0 },
      { key:41,rate:0 },
      { key:42,rate:0 },
      { key:43,rate:0 },
      { key:44,rate:0 },
      { key:45,rate:0 },
      { key:46,rate:0 },
      { key:47,rate:0 },
      { key:48,rate:0 },
      { key:49,rate:0 },
      { key:50,rate:0 }
    ],

    /**
     * 查找第一个符合filter的item
     * @param filter
     * @returns {*}
     */
    getItem: function(filter){
        var result = null;
        for(var i=0; i<this.items.length; ++i){
            if(filter(this.items[i])){
                result = this.items[i];
                return result;
            }
        }
        return result;
    },

    /**
     * 查找第一个符合filter的list
     * @param filter
     * @returns {*}
     */
    getItemList: function(filter){
        var list = new Array();
        this.items.forEach(function (item) {
            if(filter(item)){
                list.push(item);
            }
        });
        return list;
    },
};

module.exports=data_hb_mai;