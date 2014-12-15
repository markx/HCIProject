var chart = {};

chart.draw = function (id, data) {

    if(data == ""){
        data = {name:"No Data", y:0, pk:""};
    }

    var title = 'Owe<br>Me';
    if(id != 'pie-oweme'){
        title = 'Owe<br>Them'
    }

    $('#'+id ).highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: title,
            align: 'center',
            verticalAlign: 'middle',
            y: 0
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                 events: {
                    click: function (e) {
                        console.log("click on pie: "+e.point);
                        window.location.href = "/friend/"+e.point.friend_pk;
                    }
                },
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                center: ['50%', '50%']
            }
        },
        
        series: [{
            type: 'pie',
            name: 'bill',
            innerSize: '45%',
            data: data
        }]
    });
};

