
new Chart(ctx, {

    type: "bar",

    data: {

        labels,

        datasets:[{
            label:"Attendance",
            data:values,
            backgroundColor:#2E5D50,
            borderColor:#23483E,
            borderWidth:2,
            borderRadius:10,
            borerSkipped:false
        }]  
    },


    opitions:{

        responsive:true,

        plugins:{
            legend:{
                display:false
            }
        },


        scales:{
            x:{
                grid:{
                    display:false
                }
            },

            y:{
                beginAtZero:true,

                grid:{
                    color:"rgba(0,0,0,0.6)"
                }
            }
        }
    }
});