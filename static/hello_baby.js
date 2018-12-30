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

/* Takes time in seconds and puts out format m:ss */
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
            scenario_started:false,
            contents: '',
            instruction_index:0,
            timedPPIDict: {}, /*timed PPIDict */
            lastPE:{ /*each contains a copy of the full scenario.PE that is checked at different times, to use in the description of the PE
                      * Note that e.g. resp does not map 1:1 onto scenario.PE.resp as it includes secretions data as well*/
                'appearance':{'has_examined':false, 'text':"", 'time':0},
                'hr':{'has_examined':false, 'text':"", 'time':0},
                'cardiac':{'has_examined':false, 'text':'', 'time':0},
                'resp':{'has_examined':false, 'text':'', 'time':0},
                'abd':{'has_examined':false, 'text':'', 'time':0},
                'neuro':{'has_examined':false, 'text':'', 'time':0},
                'other':{'has_examined':false, 'text':'', 'time':0},
                'vent':{'has_examined':false, 'text':'', 'time':0}
            },
            
            /*this is related to popper, still needed?*/
            pl:'left',
            
            /* timers */
            baby_timer_started: false,
            delivery_time:null,
            elapsed_delivery_time:0, /*in seconds*/
            baby_time:null,
            elapsed_baby_time:null, /*in seconds*/
            baby_delivered: false,
            
            /* stand in for app data */
            scenario:{},
            
            /*action log*/
            actionLog: [],
            
            
            data_last_updated:null,
            data_updater:null, /*repeatedly update data */
            
            /* app settings */
            app_mode:"practice", /*alternatives are practice and test */
            app_state:"instruction", /* options include playing, hint */
            
            /* tabs */
            ventTab:"start",
            showTab: "None",
            actionTab: "simple",
            mainTab: "history",
            warmerTab: "warmer_settings",
            supplyTab: 'basic',
            interveneTab:"supplies",
            
            /* tasks, supplies */
            supplyToFetch: null,
            task: null,
            
            /*actions*/
            action_in_progress: {},
            
            /* messages */
            show_message:true,
            hb_message:"The baby is about to be delivered.  Time to get the warmer ready.", /*need to make this part of the scenario text*/
        },
        components: {
           'vueSlider': window['vue-slider-component'],
        },
        created: function(){
            this.getScenario();
        },
        computed: {
            sortedActionLog: function(){
                    function compare(a, b) {
                      if (a.time < b.time)
                        return -1;
                      if (a.time > b.time)
                        return 1;
                      return 0;
                    }
                    return this.actionLog.sort(compare);
            },
            getMasks: function(){
                return this.scenario.supplies.filter(function(supply){return supply.name==='mask'})
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
        methods: {  
                getPrettyPrintPE: function(PEtype){
                    var time=Date.now()
                    self=this;
                    axios.post("/getPrettyPrintPE", {"time":time, 'PPIDict':self.timedPPIDict}).then(function(response){
                        var pedict=response.data;
                        self.lastPE[PEtype].text=pedict[PEtype];
                    });
                },
                updateLastPE: function(PEtype){
                    this.lastPE[PEtype].has_examined=true;
                    if (PEtype=='hr'){
                        this.lastPE[PEtype].text=this.scenario.PE.vitals.hr;
                    }
                    else {
                        this.getPrettyPrintPE(PEtype);
                    }
                    this.lastPE[PEtype].time=Date.now();
                },
            /*gives exam, together with time that it was last updated */
                 lpe: function(PEtype){
                    var toReturn={};
                    toReturn['text']=this.lastPE[PEtype].text;
                    t=5*Math.floor((Date.now()-this.lastPE[PEtype]['time'])/5000);
                    toReturn['time']=t;
                    return toReturn;
                },
                /*Probably need to test this logic because this is sort of patched together with string*/
                convertDictToTimed(newdict, olddict, time){
                    self=this;
                    var returnDict=Object.keys(newdict).reduce(function(obj, key){
                        if ((typeof newdict[key] === 'string') || (typeof newdict[key] === 'number')){
                            if(olddict.hasOwnProperty(key)){
                                obj[key]={};
                                obj[key]['value']=newdict[key];
                                if(olddict[key]['value']!=newdict[key]){
                                    obj[key]['time']=time;   
                                }
                                else {
                                    obj[key]['time']=olddict[key]['time'];
                                }
                            }
                            else{
                                obj[key]={}
                                obj[key]['value']=newdict[key];
                                obj[key]['time']=time; 
                            }
                        }
                        else {
                            obj[key]={};
                            if(olddict.hasOwnProperty(key)){
                                obj[key]=self.convertDictToTimed(newdict[key], olddict[key], time);
                            }
                            else{
                                obj[key]=self.convertDictToTimed(newdict[key], {}, time);
                            }
                       }
                        return obj;
                    }, {});
                    return returnDict
                },
                getTimedPPIDict(newdict){
                    var time=Date.now();
                    /* if PPIdict has not yet been created */
                    if(Object.keys(this.timedPPIDict).length===0){
                        this.timedPPIDict=this.convertDictToTimed(newdict, {}, time-30000); /*this is a stupid hack*/
                    }
                    /* if dict has already been created */
                    else {
                         this.timedPPIDict=this.convertDictToTimed(newdict, this.timedPPIDict, time);
                    }
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
                        self.actionLog=self.scenario.actionLog;
                        self.app_mode=self.scenario.app_mode;
                        var ppidict=self.scenario.PPIDict;
                        self.getTimedPPIDict(ppidict);
                    });
                    
                    
                },
                startBabyTimer: function(){
                    this.simpleTask("startTimer")
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
                        this.updateLastPE('appearance');
                        this.updateLastPE('vent');
                    }
                },
                doTask: function(task){
                    /*the code below does not take into account the possibility that action is repeated in less than 5 seconds*/
                    let self=this;
                    self.action_in_progress[task.name]=true;
                    var timer=setInterval(function(){
                        self.action_in_progress[task.name]=false;
                    }, 5000);
                    
                    /*function will immediately go to use_supply if task is type 'use' */
                    if(task.name.substring(0,4)==="use_"){
                        this.useSupply({'name':task.name.substring(4), 'size':null});
                        return null;
                    }
                    
                    /*now we actually send the task to the server*/
                    var current_time=0;
                    if (this.baby_delivered) {
                        current_time=(Date.now()-this.delivery_time)/1000;
                    }
                    this.elapsed_delivery_time=current_time;
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
                  hideMessage: function(){
                    this.show_message=false;
                    this.scenario_started=true;
                  },
            
            /*I have no idea what this code below is for - Aaaah refactor_this */
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
                                self.updateLastPE('appearance');
                                self.updateLastPE('vent');
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

