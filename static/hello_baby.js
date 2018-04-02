
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
for (var i=0, max = hs.length; i < max; i++) {
    hs[i].parentNode.removeChild(hs[i]);
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
            baby:{},
            mom:{},
            warmer:{},
            supplyMGR:{},
            scenario_data:{}
        },
        created: function(){
            let self=this;
            axios.post("/getmodel", {
                model:"baby"
              }).then(function (response) {
                self.baby=response.data;
              })
            axios.post("/getmodel", {
                model:"mom"
              }).then(function (response) {
                self.mom=response.data;
              })
          axios.post("/getmodel", {
                model:"warmer"
              }).then(function (response) {
                self.warmer=response.data;
              })
          axios.post("/getmodel", {
                model:"supplyMGR"
              }).then(function (response) {
                self.supplyMGR=response.data;
              })
          axios.post("/getscenario", {
                model:"scenario_data"
              }).then(function (response) {
                self.scenario_data=response.data;
              })


        },
        mounted: function() {
            this.interval = setInterval(this.updateCurrentTime, 1000);
        },
        destroyed: function() {
            clearInterval(this.interval);
        },
        computed: {
            supplySearchOptions: function(){
                var supplyList=this.supplyMGR.supplyList;
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
                  doTask: function(){
                    var argsToSend = Array.prototype.slice.call(arguments);
                    let self=this;
                      axios.post("/doTask", {
                        args:argsToSend
                      }).then(function (response) {
                        self.updateData();
                  })
                  },
                  toggleHeat: function(){
                      this.warmer.turnedOn=!this.warmer.turnedOn;
                      this.updateWarmer();
                  },
                  updateWarmer: function(){
                      let self=this
                      axios.post("/savedata", {
                        model_name:"warmer",
                        model:JSON.stringify(self.warmer),
                      })
                  },
                  updateData: function(){
                          let self=this;
                        axios.post("/getmodel", {
                            model:"baby"
                          }).then(function (response) {
                            self.baby=response.data;
                          })
                      axios.post("/getmodel", {
                            model:"warmer"
                          }).then(function (response) {
                            self.warmer=response.data;
                          })
                      axios.post("/getmodel", {
                            model:"staff"
                          }).then(function (response) {
                            self.staff=response.data;
                          })
                      axios.post("/getmodel", {
                            model:"supplyMGR"
                          }).then(function (response) {
                            self.supplyMGR=response.data;
                          })
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

