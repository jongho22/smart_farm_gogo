/*!
    * Start Bootstrap - SB Admin v7.0.5 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2022 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

$(document).ready(function() {
    const config ={
        type: 'line',
        data: {
            labels : [],
            datasets : [{
                label : "Temperature",
                yAxisID: "A",
                backgroundColor : 'rgb(255,51,51)',
                borderColor: 'rgb(255,51,51)',
                data : [],
                fill : false,
            },{
                label : "humi",
                yAxisID: "B",
                backgroundColor : 'rgb(51,153,255)',
                borderColor: 'rgb(51,153,255)',
                data : [],
                fill : false,
            }]
        },
        options : {
            responsive : true,
            title : {
                display : true,
                text : "실시간 온습도 센서 값"
            },
            scales : {
                xAxes : [{
                    display : true,
                    scaleLabel : {
                        display : true,
                        labelString: 'Time'
                    }
                }],
                yAxes : [{
                    id: 'A',
                    display : true,
                    scaleLabel : {
                        display : true,
                        labelString: 'Temp'
                    }
                },{
                    id: 'B',
                    display : true,
                    scaleLabel : {
                        display : true,
                        labelString: 'Humi'
                    }
                }
            ]
            },
            tooltips: {
                mode : 'index',
                intersect : false,
            },
            hover : {
                mode: 'nearest',
                intersect: true
            }
        }
    };
    
    const context = document.getElementById('canvas').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/graph")
    
    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (config.data.labels.length === 30) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
            config.data.datasets[1].data.shift();
        }
        config.data.labels.push(data.time);
        config.data.datasets[0].data.push(data.value1);
        config.data.datasets[1].data.push(data.value2);
        lineChart.update();
        
        $("#temp_humi_sensor").text("온도센서 값 : "+data.value1 + " / 습도센서 값: " + data.value2);
        $("#light_sensor").text("조도센서 값 : "+data.value3+" => "+data.value3_1);
        $("#rain_sensor").text("빗물 감지 센서 값 : "+data.value4+" => "+data.value4_1);
        $("#temp_sensor_2").text(data.value1);
        $("#humi_sensor_2").text(data.value2+"%");
        $("#light_sensor_2").text(data.value3);
        $("#rain_sensor_2").text(data.value4);
    }
});

$(document).ready(function() {
    const config ={
        type: 'doughnut',
        data : {
            labels: ['조도센서','남은 센서 값'],//['온도센서','습도센서','조도센서', '빗물감지 센서'],
            datasets: [{
                data: [],
                backgroundColor: ['rgb(255, 255, 51)','rgb(230,230,230)'],//,'rgb(255, 255, 51)', 'rgb(204, 229, 255)'],
                borderColor : 'rgb(150,150,150)',
            }],
        },
        options: {
            responsive: false,
            cutoutPercentage : 50,
        },
    };
    const context = document.getElementById('canvas4').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/graph")

    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
       
        config.data.datasets[0].data.pop();
        config.data.datasets[0].data.pop();
        
        config.data.datasets[0].data.push(data.value3,1200-data.value3)//,data.value3,data.value4);
        
        lineChart.update();
    }
});

$(document).ready(function() {
    const config ={
        type: 'doughnut',
        data : {
            labels: ['온도센서','남은 센서 값'],//['온도센서','습도센서','조도센서', '빗물감지 센서'],
            datasets: [{
                data: [],
                backgroundColor: ['rgb(255,51,51)','rgb(230,230,230)'],//,'rgb(255, 255, 51)', 'rgb(204, 229, 255)'],
                borderColor : 'rgb(150,150,150)',
            }],
        },
        options: {
            responsive: false,
            cutoutPercentage : 50,
        },
    };
    const context = document.getElementById('canvas2').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/graph")

    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
       
        config.data.datasets[0].data.pop();
        config.data.datasets[0].data.pop();
        
        config.data.datasets[0].data.push(data.value1,50-data.value1)//,data.value3,data.value4);
        
        lineChart.update();
    }
});

$(document).ready(function() {
    const config ={
        type: 'doughnut',
        data : {
            labels: ['습도센서','남은 센서 값'],//['온도센서','습도센서','조도센서', '빗물감지 센서'],
            datasets: [{
                data: [],
                backgroundColor: ['rgb(51,153,255)','rgb(230,230,230)'],//,'rgb(255, 255, 51)', 'rgb(204, 229, 255)'],
                borderColor : 'rgb(150,150,150)',
            }],
        },
        options: {
            responsive: false,
            cutoutPercentage : 50,
        },
    };
    const context = document.getElementById('canvas3').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/graph")

    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
       
        config.data.datasets[0].data.pop();
        config.data.datasets[0].data.pop();
        
        config.data.datasets[0].data.push(data.value2,80-data.value2)//,data.value3,data.value4);
        
        lineChart.update();
    }
});

$(document).ready(function() {
    const config ={
        type: 'doughnut',
        data : {
            labels: ['빗물감지 센서','남은 센서 값'],//['온도센서','습도센서','조도센서', '빗물감지 센서'],
            datasets: [{
                data: [],
                backgroundColor: ['rgb(204, 229, 255)','rgb(230,230,230)'],//,'rgb(255, 255, 51)', 'rgb(204, 229, 255)'],
                borderColor : 'rgb(150,150,150)',
            }],
        },
        options: {
            responsive: false,
            cutoutPercentage : 50,
        },
    };
    const context = document.getElementById('canvas5').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/graph")

    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
       
        config.data.datasets[0].data.pop();
        config.data.datasets[0].data.pop();
        
        config.data.datasets[0].data.push(data.value4,1023-data.value4)//,data.value3,data.value4);
        
        lineChart.update();
    }
});

var Target = document.getElementById("clock");
            function clock() {
                var time = new Date();

                var month = time.getMonth();
                var date = time.getDate();
                var day = time.getDay();
                var week = ['일', '월', '화', '수', '목', '금', '토'];

                var hours = time.getHours();
                var minutes = time.getMinutes();
                var seconds = time.getSeconds();

                Target.innerText = 
                '현재 시간 : ' +
                `${month + 1}월 ${date}일 ${week[day]}요일 ` +
                `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
                    
            }
            clock();
            setInterval(clock, 1000); // 1초마다 실행
