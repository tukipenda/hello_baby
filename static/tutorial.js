Vue.component('v-select', VueSelect.VueSelect);
Vue.component('v-select-intervene', VueSelect.VueSelect);

/*There is a problem which is css is dynamically loaded based on the name of the component here.  Probably I eventually need to package this on my own
so this is not an issue
*/

var hs = document.getElementsByTagName('style');
if (hs.length) {
    for (var i = 0, max = hs.length; i < max; i++) {
        if (hs[i]) {
            hs[i].parentNode.removeChild(hs[i]);
        }
    }
}

function formatTime(t) {
    t = Math.floor(t / 1000);
    var m = Math.floor(t / 60);
    t -= m * 60;
    if (t == 0) {
        t = "00";
    } else if (t < 10) {
        t = "0" + t;
    }
    return (m + ":" + t);
}

var app = new Vue({
    el: '#HelloBabyApp',
    delimiters: ['[[', ']]'],
    data: {
        scenario_started: false,
        contents: '',
        instruct_index:0,
        tutorial_messages:tutorial_messages,
        poppers: {},
        popper_displayed: {},
        lastPE: {
            /*each contains a copy of the full scenario.PE that is checked at different times, to use in the description of the PE
             * Note that e.g. resp does not map 1:1 onto scenario.PE.resp as it includes secretions data as well*/
            'hr': {
                'has_examined': false,
                'text': "",
                'time': 0
            },
            'cardiac': {
                'has_examined': false,
                'text': '',
                'time': 0
            },
            'resp': {
                'has_examined': false,
                'text': '',
                'time': 0
            },
            'abd': {
                'has_examined': false,
                'text': '',
                'time': 0
            },
            'neuro': {
                'has_examined': false,
                'text': '',
                'time': 0
            },
            'other': {
                'has_examined': false,
                'text': '',
                'time': 0
            }
        },
        pl: 'left',
        ventTab: "start",
        drawer_opened: false,
        baby_timer_started: false,
        delivery_time: null,
        elapsed_delivery_time: 0,
        /*in seconds*/
        baby_time: null,
        elapsed_baby_time: null,
        /*in seconds*/
        baby_delivered: false,
        scenario: scenario_tutorial,
        data_last_updated: null,
        data_updater: null,
        /*repeatedly update data */
        app_mode: "practice",
        /*alternatives are practice and test */
        app_state: "instruction",
        /* options include playing, hint */
        showTab: "None",
        actionTab: "simple",
        mainTab: "history",
        warmerTab: "warmer_settings",
        interveneTab: "supplies",
        supplyToFetch: null,
        task: null,
        show_message: true,
        hb_message: "The baby is about to be delivered.  Time to get the warmer ready.",
        /*need to make this part of the scenario text*/
    },
    components: {
        'vueSlider': window['vue-slider-component'],
    },
    created: function() {
        this.getScenario();
    },
    computed: {
        availableSupplies: function() {
            var toReturn = [];
            var s = this.scenario.supplies;
            for (var i = 0; i < s.length; i++) {
                if (s[i].is_available == true) {
                    if ((s[i].name != "mask") && (s[i].name != "ett") && (s[i].name != "laryngoscope")) {
                        toReturn.push(s[i]);
                    }
                }
            }
            return toReturn;
        },
        supplySearchOptions: function() {
            var supplyList = this.scenario.supplies;
            var toReturn = [];
            for (var i = 0; i < supplyList.length; i++) {
                if (supplyList[i].is_available == false) {
                    toReturn.push(supplyList[i]);
                };
            }
            return toReturn;
        },
        getMasks: function() {
            var masks = [];
            var supplyList = this.scenario.supplies;
            for (var i = 0; i < supplyList.length; i++) {
                if (supplyList[i].name == "mask") {
                    masks.push(supplyList[i]);
                };
            }
            return masks;
        },
        is_IE: function() {
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
    mounted: function(){
        this.displayNextPopups();
    },
    updated: {

    },
    methods: {
        nextStep: function() {
            this.instruct_index+=1;
            this.displayNextPopups();
        },
        createPopper: function(msg, target_id, pl){
            var id="popper_"+target_id;
            var d1 = document.getElementById('popup_tutorials');
            d1.insertAdjacentHTML('beforeend', '<div id="'+id+'" class="popover bs-popover-'+pl+' card"><div class="arrow"></div><div class="popover-body">'+msg+'</div></div>');
            this.displayPopper(id, target_id, pl);
        },
        displayPopper: function(id, target_id, pl){
            var target=document.getElementById(target_id);
            var popover=document.getElementById(id);
            self=this;
            if(target==null){
                popover.style.display="none";
            }
            else {
                this.poppers[target_id] = new Popper(target, popover, {
                   placement: pl
                });
                target.addEventListener('click', function() {
                    self.deletePopper(target_id);
                }, false);
                setInterval(function(){ self.poppers[target_id].update(); }, 50);
            }
         },
        deletePopper: function(target_id){
            this.poppers[target_id].destroy();
            var targ_popover=document.getElementById('popper_'+target_id);
            if (targ_popover == null) {
                 //do nothing
            }
            else {
                targ_popover.parentNode.removeChild(targ_popover);
            }
        },
        displayNextPopups: function(){
            var msgs=popup_messages[this.instruct_index];
            self=this;
            if(this.instruct_index>0){
                var old=popup_messages[this.instruct_index-1];
                Object.keys(old).forEach(function(key){
                    self.deletePopper(key);
                });
            }
            Object.keys(msgs).forEach(function(key){
                self.createPopper(msgs[key].text, key, msgs[key].position);
            })
        },
        updateLastPE: function(PEtype) {
            this.lastPE[PEtype].has_examined = true;
            if (PEtype == 'hr') {
                this.lastPE[PEtype].text = this.scenario.PE.vitals.hr;
            } else {
                this.lastPE[PEtype].text = this.scenario.PEtext[PEtype];
            }
            this.lastPE[PEtype].time = Date.now();
        },
        lpe: function(PEtype) {
            var toReturn = {};
            toReturn['text'] = this.lastPE[PEtype].text;
            t = 5 * Math.floor((Date.now() - this.lastPE[PEtype]['time']) / 5000);
            toReturn['time'] = t;
            return toReturn;
        },
        getScenario: function() {
            this.data_last_updated = Date.now();
            let self = this;
            var dtime = 0;
            if (this.baby_delivered) {
                dtime = Date.now() - this.delivery_time;
            }
        },
        startBabyTimer: function() {
            this.baby_timer_started = true;
            this.baby_time = Date.now();
            this.elapsed_baby_time = "0:00";
            let self = this;
            var timer = setInterval(function() {
                ctime = Date.now();
                self.elapsed_baby_time = formatTime(ctime - self.baby_time);
            }, 1000);
        },
        deliverBaby: function() {
            if (!this.baby_delivered) {
                this.baby_delivered = true;
                this.mainTab = "resuscitation";
                this.delivery_time = Date.now();
                this.doTask({
                    'name': "deliver_baby"
                });
                this.updateData();
                this.hb_message = "The baby was just delivered!";
                this.showTab = "None";
                this.show_message = true;
            }
        },
        doTask: function(task) {
            //do nothing in tutorial mode
        },
        simpleTask: function(taskName) {
            this.doTask({
                'name': taskName
            });
        },
        checkSupplyByName: function(name, size) {
            var toReturn = null;
            var s = this.scenario.supplies;
            for (var i = 0; i < s.length; i++) {
                if ((s[i].name == name)) { /*and (s[i].size==size)){ need to implement this */
                    toReturn = s[i];
                }
            }
            return toReturn;
        },
        getSupply: function(supply) {
            var name = supply.name;
            var size = supply.size;
            supply.is_available = true;
            this.doTask({
                'name': "fetch",
                'supply_name': name,
                'size': size
            });
        },
        useSupply: function(supply) {
            myFxn = function(self, mysupply) {
                masks = self.scenario.supplies.filter(function(supply) {
                    return (supply.name === "mask");
                })
                masks.map(function(supply) {
                    supply.size != mysupply.size ? supply.is_using = false : supply.is_using = !supply.is_using;
                })
            }
            var name = supply.name;
            var size = supply.size;
            name != 'mask' ? (supply.is_using = true) : myFxn(this, supply);
            this.doTask({
                'name': "use",
                'supply_name': name,
                'size': size
            });
        },
        helloSliderOptions: function(min, max, width) {
            width = typeof width !== 'undefined' ? width : '50%';
            var options = {
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
        hideMessage: function() {
            this.show_message = false;
            this.scenario_started = true;
        },
        toggleEl: function(el_id) {
            this.toggle_values[el_id] = !this.toggle_values[el_id];
            return this.toggle_values[el_id];
        },
        get_toggle_values: function(el_id) {
            if (this.toggle_values.hasOwnProperty(el_id)) {
                return this.toggle_values[el_id];
            } else {
                Vue.set(this.toggle_values, el_id, false);
            }
        },
        toggleHeat: function() {
            this.scenario.warmer.is_turned_on = !this.scenario.warmer.is_turned_on;
            this.doTask({
                'name': "updatewarmer",
                'is_turned_on': this.scenario.warmer.is_turned_on
            });
        },
        toggleShowTab: function(name) {
            if (this.showTab === name) {
                this.showTab = "None";
            } else {
                this.showTab = name;
            }
        },
        toggleTempMode: function() {
            if (this.scenario.warmer.temp_mode == "baby") {
                this.scenario.warmer.temp_mode = "manual";
            } else {
                this.scenario.warmer.temp_mode = "baby";
            }
            this.doTask({
                'name': "updatewarmer",
                'temp_mode': this.scenario.warmer.temp_mode
            });
        },
        updateData: function() {
            this.data_last_updated = Date.now();
            self = this;
            this.data_updater = setInterval(function() {
                if ((Date.now() - self.data_last_updated) > 5000) {
                    self.getScenario();
                }
            }, 3000);
        },
        updateWarmer: function(pressure_type, pvalue) {
            pressure = pressure_type.toLowerCase()
            task = {
                'name': 'updatewarmer'
            }
            task[pressure] = pvalue
            this.doTask(task);
        }
    }
});