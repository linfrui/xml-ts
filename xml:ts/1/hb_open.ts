var data_hb_open =
{
    items:
    [
      { key:100,rate:1000,num:4 },
      { key:200,rate:1000,num:4 },
      { key:300,rate:1000,num:4 },
      { key:-100,rate:1000,num:4 },
      { key:-200,rate:1000,num:4 },
      { key:-300,rate:1000,num:4 },
      { key:101,rate:900,num:3 },
      { key:201,rate:700,num:3 },
      { key:301,rate:500,num:2 },
      { key:-101,rate:1600,num:4 },
      { key:-201,rate:2000,num:4 },
      { key:-301,rate:2200,num:3 },
      { key:110,rate:1500,num:4 },
      { key:210,rate:1800,num:3 },
      { key:310,rate:2000,num:2 },
      { key:-110,rate:800,num:2 },
      { key:-210,rate:500,num:2 },
      { key:-310,rate:400,num:1 },
      { key:111,rate:1500,num:4 },
      { key:211,rate:1500,num:4 },
      { key:311,rate:1500,num:4 },
      { key:-111,rate:1500,num:4 },
      { key:-211,rate:1500,num:4 },
      { key:-311,rate:1500,num:4 }
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

module.exports=data_hb_open;