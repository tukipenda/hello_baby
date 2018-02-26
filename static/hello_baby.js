
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

var app = new Vue({
        el: '#HelloBabyApp',
        delimiters: ['[[',']]'],
        data: {
            contents: '',
             state: "started",
                startTime: Date.now(),
                currentTime: Date.now(),
                interval: null,

            baby:{},
            mom:{},
            warmer:{},
            supplyMGR:{},
            scenario_data:{},
            staff:[]
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
                model:"staff"
              }).then(function (response) {
                self.staff=response.data;
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
                  doTask: function(taskName, parameter){
                    let self=this
                      axios.post("/doTask", {
                        task_name:taskName,
                        parameter:parameter,
                      }).then(function (response) {
                    alert(response.data);
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

