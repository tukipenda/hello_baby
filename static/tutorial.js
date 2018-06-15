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

scenario_tutorial={"scenario_text":"You are called by the OB team for a stat C/S. Mom is 25 years old, and gestational age is 32 weeks.",
"PE":
    {"vitals":{"o2sat":55,"o2sat_updated":0,"hr":120,"rr":0,"sbp":75,"dbp":50,"temp":35,"weight":2.25},
    "resp":{"breath_sounds":"None","chest_rise":"None","wob":"None","is_grunting":false,"is_spontaneous":false},
    "cardiac":{"murmur":"no murmur","sounds":"normal S1/S2","femoral_pulse":"2+","brachial_pulse":"2+"},
    "secretions":{"quantity":"moderate","below_cords":false,"color":"clear","thickness":"thin"},
    "abd":{"bs":"+bs","palpate":"soft, no HSM"},"neuro":{"loc":"no cry","motor_activity":"not moving","motor_deficit":"none"},
    "skin":{"color":"blue","is_dry":false,"texture":"term infant skin"},
    "other":{"scalp":"no caput","clavicles":"no clavicular fracture","ears":"normally positioned","eyes":"red reflex intact bilaterally",
        "umbilical_cord":"normal 3 vessel cord","palate":"palate intact","lips":"no cleft lips","gu":"normal genitalia","hips":"no hip click",
        "spine":"no dimple","anus":"patent anus"}},
"resusc":{
    "vent":{"efficacy":0,"is_mouth_open":false,"positioning":0,"is_airway_open":true,"has_air_leak":false,"set_rate":"0","vent_type":"spontaneous"},
    "cpr":{"event_rate":0,"btc_breaths":0,"btc_compressions":0,"cpr_depth":"0","efficacy":0},
    "uvc":{"is_uvc_placed":false,"medications_given":"[]"}},
"mom":{"age":25,"PNL":"Prenatal labs: VZVI, RI, HIV negative, Hep B negative, RPRNR, GC/Chlamydia negative","hsv":"No history of HSV and has no active lesions.","gbs":"GBS+.  She was febrile to 38.1, and received ampicillin 2 hours before delivery.","rom":"ROM occurred 16 hours ago.","gp":"G1PO"},
"baby":{"ga":"32","neonatal_complications":"None","is_delivered":null},"warmer":{"is_turned_on":false,"suction":0,"fio2":100,"flow":0,"temp_mode":"manual","peep":0,"pip":0,"pop":0},
"supplies":[{"size":null,"name":"pulse_ox","is_available":false,"is_using":false,"pp":"pulse_ox"},{"size":null,"name":"hat","is_available":false,"is_using":false,"pp":"hat"},{"size":null,"name":"transwarmer","is_available":false,"is_using":false,"pp":"transwarmer"},{"size":null,"name":"plastic_bag","is_available":false,"is_using":false,"pp":"plastic_bag"},{"size":null,"name":"temp_probe","is_available":false,"is_using":false,"pp":"temp_probe"},{"size":null,"name":"blankets","is_available":false,"is_using":false,"pp":"blankets"},{"size":null,"name":"bulb_suction","is_available":false,"is_using":false,"pp":"bulb_suction"},{"size":null,"name":"meconium_aspirator","is_available":false,"is_using":false,"pp":"meconium_aspirator"},{"size":null,"name":"stethoscope","is_available":false,"is_using":false,"pp":"stethoscope"},{"size":null,"name":"epinephrine","is_available":false,"is_using":false,"pp":"epinephrine"},{"size":null,"name":"normal_saline_bag","is_available":false,"is_using":false,"pp":"normal_saline_bag"},{"size":null,"name":"cord_clamp","is_available":false,"is_using":false,"pp":"cord_clamp"},{"size":null,"name":"scalpel","is_available":false,"is_using":false,"pp":"scalpel"},{"size":null,"name":"flush","is_available":false,"is_using":false,"pp":"flush"},{"size":null,"name":"UVC","is_available":false,"is_using":false,"pp":"UVC"},{"size":"0","name":"laryngoscope","is_available":false,"is_using":false,"pp":"laryngoscope: 0"},{"size":"1","name":"laryngoscope","is_available":false,"is_using":false,"pp":"laryngoscope: 1"},{"size":"00","name":"laryngoscope","is_available":false,"is_using":false,"pp":"laryngoscope: 00"},{"size":"2.5","name":"ett","is_available":false,"is_using":false,"pp":"ett: 2.5"},{"size":"3","name":"ett","is_available":false,"is_using":false,"pp":"ett: 3"},{"size":"3.5","name":"ett","is_available":false,"is_using":false,"pp":"ett: 3.5"},{"size":"Infant","name":"mask","is_available":true,"is_using":false,"pp":"mask: Infant"},{"size":"Preemie","name":"mask","is_available":true,"is_using":false,"pp":"mask: Preemie"}],"tasks":[{"name":"fetch","supply_name":"pulse_ox","size":null,"pp":"fetch pulse_ox"},{"name":"fetch","supply_name":"hat","size":null,"pp":"fetch hat"},{"name":"fetch","supply_name":"transwarmer","size":null,"pp":"fetch transwarmer"},{"name":"fetch","supply_name":"plastic_bag","size":null,"pp":"fetch plastic_bag"},{"name":"fetch","supply_name":"temp_probe","size":null,"pp":"fetch temp_probe"},{"name":"fetch","supply_name":"blankets","size":null,"pp":"fetch blankets"},{"name":"fetch","supply_name":"bulb_suction","size":null,"pp":"fetch bulb_suction"},{"name":"fetch","supply_name":"meconium_aspirator","size":null,"pp":"fetch meconium_aspirator"},{"name":"fetch","supply_name":"stethoscope","size":null,"pp":"fetch stethoscope"},{"name":"fetch","supply_name":"epinephrine","size":null,"pp":"fetch epinephrine"},{"name":"fetch","supply_name":"normal_saline_bag","size":null,"pp":"fetch normal_saline_bag"},{"name":"fetch","supply_name":"cord_clamp","size":null,"pp":"fetch cord_clamp"},{"name":"fetch","supply_name":"scalpel","size":null,"pp":"fetch scalpel"},{"name":"fetch","supply_name":"flush","size":null,"pp":"fetch flush"},{"name":"fetch","supply_name":"UVC","size":null,"pp":"fetch UVC"},{"name":"fetch","supply_name":"laryngoscope","size":"0","pp":"fetch laryngoscope: 0"},{"name":"fetch","supply_name":"laryngoscope","size":"1","pp":"fetch laryngoscope: 1"},{"name":"fetch","supply_name":"laryngoscope","size":"00","pp":"fetch laryngoscope: 00"},{"name":"fetch","supply_name":"ett","size":"2.5","pp":"fetch ett: 2.5"},{"name":"fetch","supply_name":"ett","size":"3","pp":"fetch ett: 3"},{"name":"fetch","supply_name":"ett","size":"3.5","pp":"fetch ett: 3.5"},{"name":"fetch","supply_name":"mask","size":"Infant","pp":"fetch mask: Infant"},{"name":"fetch","supply_name":"mask","size":"Preemie","pp":"fetch mask: Preemie"},{"name":"use","supply_name":"pulse_ox","size":null,"pp":"use pulse_ox"},{"name":"use","supply_name":"hat","size":null,"pp":"use hat"},{"name":"use","supply_name":"transwarmer","size":null,"pp":"use transwarmer"},{"name":"use","supply_name":"plastic_bag","size":null,"pp":"use plastic_bag"},{"name":"use","supply_name":"temp_probe","size":null,"pp":"use temp_probe"},{"name":"use","supply_name":"blankets","size":null,"pp":"use blankets"},{"name":"use","supply_name":"bulb_suction","size":null,"pp":"use bulb_suction"},{"name":"use","supply_name":"meconium_aspirator","size":null,"pp":"use meconium_aspirator"},{"name":"use","supply_name":"stethoscope","size":null,"pp":"use stethoscope"},{"name":"use","supply_name":"epinephrine","size":null,"pp":"use epinephrine"},{"name":"use","supply_name":"normal_saline_bag","size":null,"pp":"use normal_saline_bag"},{"name":"use","supply_name":"cord_clamp","size":null,"pp":"use cord_clamp"},{"name":"use","supply_name":"scalpel","size":null,"pp":"use scalpel"},{"name":"use","supply_name":"flush","size":null,"pp":"use flush"},{"name":"use","supply_name":"UVC","size":null,"pp":"use UVC"},{"name":"use","supply_name":"laryngoscope","size":"0","pp":"use laryngoscope: 0"},{"name":"use","supply_name":"laryngoscope","size":"1","pp":"use laryngoscope: 1"},{"name":"use","supply_name":"laryngoscope","size":"00","pp":"use laryngoscope: 00"},{"name":"use","supply_name":"ett","size":"2.5","pp":"use ett: 2.5"},{"name":"use","supply_name":"ett","size":"3","pp":"use ett: 3"},{"name":"use","supply_name":"ett","size":"3.5","pp":"use ett: 3.5"},{"name":"use","supply_name":"mask","size":"Infant","pp":"use mask: Infant"},{"name":"use","supply_name":"mask","size":"Preemie","pp":"use mask: Preemie"},{"name":"dry","pp":"dry"},{"name":"stimulate","pp":"stimulate"},{"name":"bulb_suction","pp":"bulb_suction"},{"name":"deep_suction","pp":"deep_suction"}],"PEtext":{"appearance":"32 week old infant.  Skin is blue and not dry. Term infant skin. Infant is not breathing. There is no chest rise. Mouth is closed. Infant is lying flat, no chin lift or jaw thrust.","resp":"Infant is not breathing. There are no breath sounds. There is no chest rise. Secretions are moderate, thin, and clear. ","cardiac":"Normal s1/s2. There is no murmur. Pulses are 2+ brachial and 2+ femoral. Heart rate is 120.","abd":"Abdomen is soft, no HSM. +bs.","neuro":"Infant is not crying. Infant is not moving.","other":"Infant does not have a caput. No clavicular fracture. Ears are normally positioned. Red reflex intact bilaterally. Normal 3 vessel cord. Palate intact. No cleft lips. Normal genitalia. No hip click. No dimple. Patent anus"},"app_mode":"practice"}

var app = new Vue({
        el: '#HelloBabyApp',
        delimiters: ['[[',']]'],
        data: {
            scenario_started:false,
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
            scenario:scenario_tutorial,
            data_last_updated:null,
            data_updater:null, /*repeatedly update data */
            app_mode:"practice", /*alternatives are practice and test */
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
        methods: {
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
                    //do nothing in tutorial mode
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
                      myFxn=function(self, mysupply){
                          masks=self.scenario.supplies.filter(function(supply){
                                return (supply.name==="mask");
                            })
                            masks.map(function(supply){
                                supply.size!=mysupply.size ? supply.is_using=false : supply.is_using=!supply.is_using;
                            })
                      }
                      var name=supply.name;
                      var size=supply.size;
                      name!='mask' ? (supply.is_using=true):myFxn(this, supply);
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

