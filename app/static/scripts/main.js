$( "#dialog-form" ).css('display','none');

$(function(){

    getCrypto();

    var dialog, form;
    
    // $( "#dialog-form" ).css('display','flex');
    dialog = $( "#dialog-form" ).dialog({
        autoOpen: false,
        height: 600,
        width: 450,
        modal: true,
        buttons: {
          "Agregar": function(){
              console.log(form);
              form.submit();
              dialog.dialog('close');
          },
          "Cancelar": function() {
            dialog.dialog( "close" );
          }
        },
        close: function() {
          form[ 0 ].reset();
        }
      });
      

      form = dialog.find( "form" )

    $( ".agregar" ).button().on( "click", function() {
        dialog.dialog( "open" );    
      });

      $(".ui-dialog-titlebar-close").html("X");
});



function getCrypto(){
    $.get('/api/crypto')
    .then(function(data){
        
        //OBTENGO ARRAY CON TODOS LOS PRECIOS DE BINANCE
        var precios;
        getBinancePrices().then(function(data){ precios = data}).then(function(){
        getHistoricalMonthPrices().then(data=> console.log(data));


            

            for (var i=0; i< data.length; i++){
                carteraContainer = $('<div class="cartera-container"></div>');
                carteraRow = $('<div class="cartera-row"></div>');
                //DATOS DE BACK-END GUARDADOS AL MOMENTO DE COMPRA
                carteraRow.append("<div class='ticker'><img src='../static/icons/svg/color/"+data[i].ticker+".svg'/>" + data[i].ticker + "<span class='tooltiptext'>Fecha Compra"+ data[i].fecha_compra + "</span></div>");
                carteraRow.append("<div>" + data[i].cantidad + " " + data[i].ticker +"<span class='tooltiptext'>Cantidad </span></div>");
                carteraRow.append("<div>" + data[i].precio_compra_usd + " $<span class='tooltiptext'>Precio Compra USD</span></div>");
                carteraRow.append("<div>" + data[i].precio_compra + " " + data[i].moneda_compra + "<span class='tooltiptext'>Precio Compra Moneda </span></div>");
                //PRECIOS DE BINANCE
                
                precioMoneda = precios.find(x => x.symbol == data[i].ticker+data[i].moneda_compra);
                precioUsd = precios.find(x => x.symbol == data[i].ticker+"USDT") || {"price":"100.0000000"};
                precioBtc = precios.find(x => x.symbol == data[i].ticker+"BTC");

                console.log(precioUsd);
                carteraRow.append("<div>" + precioUsd.price.slice(0,precioUsd.price.length - 6) + " $<span class='tooltiptext'>Precio $</span></div>");
                carteraRow.append("<div>" + precioBtc.price + " BTC<span class='tooltiptext'>Precio BTC</span></div>");
                carteraRow.append("<div>" + precioMoneda.price +" "+ data[i].moneda_compra +"<span class='tooltiptext'>Precio Moneda </span></div>");
                
                carteraRow2 = $('<div class="cartera-row"></div>');
                //% de variacion desde compra
                let desdeCompraUsd = (precioUsd.price/data[i].precio_compra_usd).toFixed(2);
                let desdeCompraMoneda = (precioMoneda.price/data[i].precio_compra).toFixed(2);
                let desdeMesUsd = (precioMoneda.price/data[i].precio_compra).toFixed(2);
                let desdeMesMoneda = (precioMoneda.price/data[i].precio_compra).toFixed(2);
                let desdeAnoUsd = (precioMoneda.price/data[i].precio_compra).toFixed(2);
                let desdeAnoMoneda = (precioMoneda.price/data[i].precio_compra).toFixed(2);

                carteraRow2.append("<div>" + desdeCompraUsd + " %<span class='tooltiptext'>% Desde Compra $</span></div>");
                carteraRow2.append("<div><span class='tooltiptext'>% Desde Compra Moneda</span></div>");
                carteraRow2.append("<div><span class='tooltiptext'>% Mes $</span></div>");
                carteraRow2.append("<div><span class='tooltiptext'>% Mes Moneda</span></div>");
                carteraRow2.append("<div><span class='tooltiptext'>% Año $</span></div>");
                carteraRow2.append("<div><span class='tooltiptext'>% Año Moneda</span></div>");
                //TOTAL
                carteraRow2.append("<div><span class='tooltiptext'>Total</span></div>");
                carteraContainer.append(carteraRow,carteraRow2);
                $('.cartera').append(carteraContainer);
            }

            $('.cartera').fadeIn().append(carteraContainer);

            $('.spin-loader').fadeOut();
    })
    .catch(function(err){
        console.log(err);
    });
    })
};


function getBinancePrices(){
    return $.get("https://api.binance.com/api/v3/ticker/price")
};

function getHistoricalMonthPrices(){
    let today = new Date() 
    let firstDayOfMonth = new Date(today.getFullYear, today.getMonth, 1);
    var timeStamp = Math.round(firstDayOfMonth.getTime()/1000);
    return $.get("https://min-api.cryptocompare.com/data/pricehistorical?fsym=BTC&tsyms=BTC,USD,EUR&ts=1514774941&extraParams=your_app_name");
}

function getPriceCryptoCompare(ticker){
    return $.get("https://min-api.cryptocompare.com/data/price?fsym="+ticker+"&tsyms=BTC,USD,ETH");
}



{/*         <div class="cartera-container">
                <div class="cartera-row">
                    <p class="ticker">ETH</p>
                    <p>1 ETH<span class="tooltiptext">Cantidad</span></p>
                    <p>0.095000 BTC<span class="tooltiptext">Precio Compra Moneda: </span></p>
                    <p>1200 $<span class="tooltiptext">Precio Compra $:</span></p>
                    <p>1250 $<span class="tooltiptext">Precio $:</span></p>
                    <p>0.0950000 BTC<span class="tooltiptext">Precio BTC: </span></p>
                    <p>0.095000 BTC<span class="tooltiptext">Precio Moneda: </span></p>
                </div>
                <div class="cartera-row">
                    <p>+ 10%<span class="tooltiptext">% desde compra $:</span></p>
                    <p>+ 10%<span class="tooltiptext">% desde compra Moneda:</span></p>
                    <p>+ 10%<span class="tooltiptext">% del mes $: </span></p>
                    <p>+ 10%<span class="tooltiptext">% del mes Moneda:</span></p>
                    <p>+ 10%<span class="tooltiptext">% del año $:</span></p>
                    <p>+ 10%<span class="tooltiptext">% del año Moneda:</span></p>
                    <p class="total">1250$<span class="tooltiptext">Total $:</span></p>
                </div>
            </div> */}


