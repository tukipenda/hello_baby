Vue.component('v-select', VueSelect.VueSelect);
Vue.component('v-select-intervene', VueSelect.VueSelect);

/*There is a problem which is css is dynamically loaded based on the name of the component here.  Probably I eventually need to package this on my own
so this is not an issue
*/


var hs = document.getElementsByTagName('style');
if(hs.length){
for (var i=0, max = hs.length; i < max; i++) {
    if(hs[i]){
        hs[i].parentNode.removeChild(hs[i]);
    }
}
}

function formatTime(t){
    t=Math.floor(t/1000);
    var m = Math.floor(t / 60);
    t -= m * 60;
    if(t==0){ t="00";}
    else if(t<10){ t="0"+t;}
    return (m+":"+t);
}

var app = new Vue({
        el: '#HelloBabyApp',
        delimiters: ['[[',']]'],
        data: {
            contents: '',
            baby_timer_started: false,
            delivery_time:null,
            baby_time:null,
            elapsed_baby_time:null, /*in seconds*/
            baby_delivered: false,
            scenario:{},
            data_last_updated:null,
            data_updater:null, /*repeatedly update data */
            showTab: "None",
            mainTab: "history",
            interveneTab:"supplies",
            supplyToFetch: null,
            task: null,
            show_message:true,
            hb_message:"The baby is about to be delivered.  Time to get the warmer ready.", /*need to make this part of the scenario text*/
            lastExam: {
                'abd':null,
                'cardiac':null,
                'resp':null
            },
        },
        components: {
           'vueSlider': window['vue-slider-component'],
        },
        created: function(){
            this.getScenario();
        },
        computed: {
            availableSupplies: function(){
                var toReturn=[];
                var s=this.scenario.supplies;
                for (var i=0;i<s.length;i++){
                    if(s[i].is_available==true){
                        toReturn.push(s[i]);
                    }
                }
                return toReturn;
            },
            supplySearchOptions: function(){
                var supplyList=this.scenario.supplies;
                var toReturn=[];
                for (var i=0;i<supplyList.length;i++){
                    if(supplyList[i].is_available==false){
                        toReturn.push(supplyList[i]);
                    };
                }
                return toReturn;
            },
            getMasks: function(){
                var masks=[];
                var supplyList=this.scenario.supplies;
                for (var i=0;i<supplyList.length;i++){
                    if(supplyList[i].name=="mask"){
                        masks.push(supplyList[i]);
                    };
                }
                return masks;
            },
            is_IE: function(){
                        var ua = window.navigator.userAgent;

                    var msie = ua.indexOf('MSIE ');
                    if (msie > 0) {
                        // IE 10 or older => return version number
                        return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
                    }

                    var trident = ua.indexOf('Trident/');
                    if (trident > 0) {
                        // IE 11 => return version number
                        var rv = ua.indexOf('rv:');
                        return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
                    }

                    var edge = ua.indexOf('Edge/');
                    if (edge > 0) {
                       // Edge (IE 12+) => return version number
                       return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
                    }

                    // other browser
                    return false;
            }
        },
        mounted: function(){ /*should really set this up so clicking the close button starts this timer*/
            self=this;
            setTimeout(
                function() {
                  self.deliverBaby();
                }, 60000);
        },
        methods: {
                getLastExam: function(PEtype){
                    this.lastExam[PEtype]=JSON.stringify(this.scenario.PE[PEtype]);
                },
                getScenario: function(){
                    this.data_last_updated=Date.now();
                    let self=this;
                    var dtime=0;
                    if(typeof this.delivery_time !== 'undefined'){
                        dtime=Date.now()-this.delivery_time;
                    }
                    var w=this.scenario.warmer;
                    this.updateWarmer(function(){
                        axios.post("/getscenario", {"time":dtime}).then(function(response){
                        self.scenario=response.data;
                        if(typeof w !== "undefined"){
                            self.scenario.warmer=w; /* terrible*/   
                        }
                    });
                    }); /*This is super hacky and needs to be improved */
                },
                startBabyTimer: function(){
                    this.baby_timer_started=true;
                    this.baby_time=Date.now();
                    this.elapsed_baby_time="0:00";
                    let self=this;
                    var timer=setInterval(function(){
                        ctime=Date.now();
                        self.elapsed_baby_time=formatTime(ctime-self.baby_time);
                    }, 1000);
                },
                deliverBaby: function(){
                    if(!this.baby_delivered){
                        this.baby_delivered=true;
                        this.mainTab="resuscitation";
                        this.doTask({'name':"deliver_baby"});
                        this.delivery_time=Date.now();
                        this.updateData();
                        this.hb_message="The baby was just delivered!";
                        this.showTab="None";
                        this.show_message=true;
                    }
                },
                doTask: function(task){
                    console.log(task);
                    let self=this;
                    axios.post("/dotask",
                             {'task':task,
                             'time':(Date.now()-this.delivery_time),
                             }).then(function(response){
                       self.getScenario();
                    });
                },
                checkSupplyByName: function(name, size){
                    var toReturn=null;
                    var s=this.scenario.supplies;
                    for (var i=0;i<s.length;i++){
                        if((s[i].name==name)){ /*and (s[i].size==size)){ need to implement this */
                            toReturn=s[i];
                        }
                    }
                    return toReturn;
                },
                  getSupply: function(supply){
                      var name=supply.name;
                      var size=supply.size;
                      supply.is_available=true;
                      this.doTask({'name':"fetch", 'supply_name':name, 'size':size});
                  },
                  useSupply: function(supply){
                      var name=supply.name;
                      var size=supply.size;
                      this.doTask({'name':"use", 'supply_name':name, 'size':size});
                  },
                  helloSliderOptions: function(min, max, width){
                      width = typeof width !== 'undefined' ? width : '50%';
                      var options={
                        eventType: 'auto',
                        width: width,
                        height: 6,
                        data: null,
                        dotHeight: null,
                        dotWidth: null,
                        min: min,
                        max: max,
                        show: true,
                        speed: 0.4,
                        disabled: false,
                        piecewiseLabel: true,
                        tooltip: "always",
                        tooltipDir: 'top',
                        reverse: false,
                        clickable: true,
                        realTime: false,
                        lazy: true,
                        formatter: null,
                        bgStyle: null,
                        processStyle: null,
                        piecewiseActiveStyle: null,
                        piecewiseStyle: null,
                        tooltipStyle: null,
                        labelStyle: null,
                        labelActiveStyle: null
                      };

                    return options;
                  },
                  toggleHeat: function(){
                      this.scenario.warmer.is_turned_on=!this.scenario.warmer.is_turned_on;
                      this.updateWarmer();
                  },
                  toggleShowTab: function(name){
                      if(this.showTab===name){
                          this.showTab="None";
                      }
                      else {
                          this.showTab=name;
                      }
                  },
                  toggleTempMode: function(){
                        if(this.scenario.warmer.temp_mode=="baby"){
                            this.scenario.warmer.temp_mode="manual";
                        }

                        else {
                            this.scenario.warmer.temp_mode="baby";
                        }
                        this.updateWarmer();
                    },
                  updateData: function(){
                      this.data_last_updated=Date.now();
                      self=this;
                      this.data_updater=setInterval(function(){
                            if((Date.now()-self.data_last_updated)>5000){
                                self.getScenario();
                            }
                        }, 3000);
                  },
                  updateWarmer: function(callbackFxn){
                      if(typeof callbackFxn === 'undefined'){
                          callbackFxn=function(){
                              return 0;
                          };
                      }
                     
                      let self=this;
                      axios.post("/updatewarmer", {
                        'warmer':JSON.stringify(self.scenario.warmer),
                      }).then(callbackFxn());
                  }
            }
        });

