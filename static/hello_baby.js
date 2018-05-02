
/*
heatOn: false,
pip:0,
peep:0,
pop:0,
pflow:0,
fio2:100,
suction:0,
supplies: ["ETT","pulse ox", "laryngoscope"],
appearance: "Infant is not crying.  Tone is poor. Infant is blue.  Not breathing.",
staff: [{name:"Raquel",role:"RT"},{name:"Desmond",role:"RN"}],
*/


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


var app = new Vue({
        el: '#HelloBabyApp',
        delimiters: ['[[',']]'],
        data: {
            contents: '',
            state: "paused",
            startTime: null,
            currentTime: null,
            interval: null,
            baby_timer_started: false,
            baby_delivered: false,
            scenario:{},
            test: 0,
            showTab: "warmer",
            supplyToFetch: null
        },
        components: {
           'vueSlider': window['vue-slider-component'],
        },
        created: function(){
            this.getScenario();
        },
        mounted: function() {
            this.interval = setInterval(this.updateCurrentTime, 1000);
        },
        destroyed: function() {
            clearInterval(this.interval);
        },
        computed: {
            availableSupplies: function(){
                var toReturn=[];
                var s=this.supplyList;
                for (var i=0;i<s.length;i++){
                    if(s[i].available==true){
                        toReturn.push(s[i]);
                    }
                }
                return toReturn;
            },
            supplySearchOptions: function(){
                var supplyList=this.supplyList;
                var toReturn=[];
                for (var i=0;i<supplyList.length;i++){
                    if(supplyList[i].available==false){
                        toReturn.push(supplyList[i]);
                    };
                }
                return toReturn;
            },
            time: function() {
                return this.minutes + ':' + this.seconds;
            },
            milliseconds: function() {
                return this.currentTime - this.$data.startTime;
            },
            minutes: function() {
                var lapsed = this.milliseconds;
                var min = Math.floor((lapsed / 1000 / 60) % 60);
                return min >= 10 ? min : '0' + min;
            },
            seconds: function() {
                var lapsed = this.milliseconds;
                var sec = Math.ceil((lapsed / 1000) % 60);
                return sec >= 10 ? sec : '0' + sec;
            }
        },
        methods: {
                getScenario: function(){
                    let self=this;
                    axios.get("/getscenario").then(function(response){
                        self.scenario=response.data;
                    });
                },
                getSupplyNames: function(){
                  /*  console.log("options");
                    var s=this.supplySearchOptions;
                for (var i=0;i<s.length;i++){
                    console.log(s[i].pp);

                }

                console.log("\nfetched");
                s=this.availableSupplies;
                for (var i=0;i<s.length;i++){
                        console.log(s[i].pp);
                }*/

                console.log("\nall");
                s=this.supplyList;
                for (var i=0;i<s.length;i++){
                    if(s[i].available==true){
                        console.log(s[i].pp);
                    };
                }

                },
                testing: function(){
                    s=this.supplyList;
                    for(i=0; i<s.length;i++){
                        this.getSupply(s[i]);
                        console.log(s[i].name);
                        a=this.availableSupplies;
                        b=this.supplySearchOptions;
                        ab=[];
                        for(var j=0;j<a.length;j++){
                            ab.push(a[j].name);
                        }
                        console.log("available");
                        console.log(ab);
                        bb=[];
                        console.log("");
                        console.log("unused");
                        for(var j=0;j<b.length;j++){
                            bb.push(b[j].name);
                        }
                        console.log(bb);
                    }

                },
                startBabyTimer: function(){
                    this.baby_timer_started=true;
                    this.state="started";
                    this.startTime=Date.now();
                    this.currentTime=Date.now();
                },
                deliverBaby: function(){
                    this.baby_delivered=true;
                },
                buttonClick: function(link){
                    let self=this;
                    axios.get(link)
                        .then(function (response) {
                            self.contents=response.data;
                            self.display=false; //need to fix this if there is ever a button taking us back to the start
                            console.log(response.data);
                        })
                        .catch(function (error) {
                            console.log(error.message);
                        });
                  },
                  getSupply: function(supply){
                      var name=supply.name;
                      var size=supply.size;
                      console.log(supply.name);
                      supply.available=true;
                      this.doTask("fetch", {'name':name, 'size':size});
                  },
                  doTask: function(name, kv){
                    let self=this;
                      axios.post("/doTask", {'taskName':name, "kv":kv}).then(function (response) {
                        self.updateData();
                  });
                  },
                  helloSliderOptions: function(min, max, width='50%'){
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
                      this.warmer.turnedOn=!this.warmer.turnedOn;
                      this.updateWarmer();
                  },
                  updateWarmer: function(){
                      let self=this;
                      axios.post("/savedata", {
                        model_name:"warmer",
                        model:JSON.stringify(self.warmer),
                      });
                  },
                  useMask: function(maskSize){
                    this.doTask("useMask", {"size":maskSize});
                  },
              reset: function() {
                    this.$data.state = "started";
                    this.$data.startTime = Date.now();
                    this.$data.currentTime = Date.now();
                },
            pause: function() {
                this.$data.state = "paused";
            },
            resume: function() {
                this.$data.state = "started";
            },
            updateCurrentTime: function() {
                if (this.$data.state == "started") {
                    this.currentTime = Date.now();
                }
            }
            }
        });

