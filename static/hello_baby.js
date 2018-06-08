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
            instruction_index:0,
            lastPE:{ /*each contains a copy of the full scenario.PE that is checked at different times, to use in the description of the PE
                      * Note that e.g. resp does not map 1:1 onto scenario.PE.resp as it includes secretions data as well*/
                'hr':{'has_examined':false, 'text':"", 'time':0},
                'cardiac':{'has_examined':false, 'text':'', 'time':0},
                'resp':{'has_examined':false, 'text':'', 'time':0},
                'abd':{'has_examined':false, 'text':'', 'time':0},
                'neuro':{'has_examined':false, 'text':'', 'time':0},
                'other':{'has_examined':false, 'text':'', 'time':0}
            },
            pl:'left',
            ventTab:"start",
            drawer_opened: false,
            baby_timer_started: false,
            delivery_time:null,
            elapsed_delivery_time:0, /*in seconds*/
            baby_time:null,
            elapsed_baby_time:null, /*in seconds*/
            baby_delivered: false,
            scenario:{},
            data_last_updated:null,
            data_updater:null, /*repeatedly update data */
            app_mode:"tutorial", /*alternatives are practice and test */
            app_state:"instruction", /* options include playing, hint */
            showTab: "None",
            actionTab: "simple",
            mainTab: "history",
            warmerTab: "warmer_settings",
            interveneTab:"supplies",
            supplyToFetch: null,
            task: null,
            show_message:true,
            hb_message:"The baby is about to be delivered.  Time to get the warmer ready.", /*need to make this part of the scenario text*/
        },
        components: {
           'vueSlider': window['vue-slider-component'],
        },
        created: function(){
            this.getScenario();
            this.$root.$emit('bv::hide::popover');
        },
        computed: {
            availableSupplies: function(){
                var toReturn=[];
                var s=this.scenario.supplies;
                for (var i=0;i<s.length;i++){
                    if(s[i].is_available==true){
                        if ((s[i].name!="mask") && (s[i].name!="ett") && (s[i].name!="laryngoscope")){
                            toReturn.push(s[i]);
                        }
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
            getPopover: function(){
                return tutorial_instructions[this.instruction_index];
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
            /* baby does not automatically deliver for now
            setTimeout(
                function() {
                  self.deliverBaby();
                }, 60000);
              */
        },
        updated: function(){
            this.loadPopup();
        },
        methods: {
                loadPopup: function(){
                    instruct_index=this.instruction_index;
                    this.$root.$emit('bv::show::popover', tutorial_instructions[instruct_index]['id']);
                    if(this.instruction_index<tutorial_instructions.length){
                        this.instruction_index+=1;
                    }
                },
                updateLastPE: function(PEtype){
                    this.lastPE[PEtype].has_examined=true;
                    if (PEtype=='hr'){
                        this.lastPE[PEtype].text=this.scenario.PE.vitals.hr;
                    }
                    else {
                        this.lastPE[PEtype].text=this.scenario.PEtext[PEtype];
                    }
                    this.lastPE[PEtype].time=Date.now();
                },
                 lpe: function(PEtype){
                    var toReturn={};
                    toReturn['text']=this.lastPE[PEtype].text;
                    t=5*Math.floor((Date.now()-this.lastPE[PEtype]['time'])/5000);
                    toReturn['time']=t;
                    return toReturn;
                },
                getScenario: function(){
                    this.data_last_updated=Date.now();
                    let self=this;
                    var dtime=0;
                    if(this.baby_delivered){
                        dtime=Date.now()-this.delivery_time;
                    }
                    axios.post("/getscenario", {"time":dtime}).then(function(response){
                        self.scenario=response.data;
                    });
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
                        this.delivery_time=Date.now();
                        this.doTask({'name':"deliver_baby"});
                        this.updateData();
                        this.hb_message="The baby was just delivered!";
                        this.showTab="None";
                        this.show_message=true;
                    }
                },
                doTask: function(task){
                    let self=this;
                    var current_time=0;
                    if (this.baby_delivered) {
                        current_time=(Date.now()-this.delivery_time)/1000;
                    }
                    this.elapsed_delivery_time=current_time;
                    console.log(task);
                    axios.post("/dotask",
                             {'task':task,
                             'time':current_time,
                             }).then(function(response){
                       self.getScenario();
                    });
                },
                simpleTask: function(taskName){
                    this.doTask({'name':taskName});
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
                  toggleEl: function(el_id){
                      this.toggle_values[el_id]=!this.toggle_values[el_id];
                      return this.toggle_values[el_id];
                  },
                  get_toggle_values: function(el_id){
                       if ( this.toggle_values.hasOwnProperty(el_id)){
                          return this.toggle_values[el_id];
                      }
                      else{
                          Vue.set(this.toggle_values, el_id, false);
                      }
                  },
                  toggleHeat: function(){
                      this.scenario.warmer.is_turned_on=!this.scenario.warmer.is_turned_on;
                      this.doTask({'name':"updatewarmer", 'is_turned_on':this.scenario.warmer.is_turned_on});
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
                        this.doTask({'name':"updatewarmer", 'temp_mode':this.scenario.warmer.temp_mode});
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
                  updateWarmer: function(pressure_type, pvalue){
                      pressure=pressure_type.toLowerCase()
                      task={'name':'updatewarmer'}
                      task[pressure]=pvalue
                      this.doTask(task);
                  }
            }
        });

