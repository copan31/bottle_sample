<!DOCTYPE html>
<html lang="ja">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <!--IEの互換モードをOFF-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <!--スマホ向けの設定-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    <title>Stock Maneger</title>
</head>

<body>
    <div class="container">

    <div class="well well-lg">
        <h1 class="panel-title">Buy</h1>
        <form class="form-inline">
        <div class="form-group">
            <label class="control-label">code:</label>
            <input id="code" type="textarea" class="form-control input-sm">
        </div>
        <div class="form-group">
            <label class="control-label">price:</label>
            <input id="buy_price" type="textarea" class="form-control input-sm">
        </div>
        <div class="form-group">
            <label class="control-label">count:</label>
            <input id="buy_count" type="textarea" class="form-control input-sm">
        </div>
        <div class="form-group">
           <label class="control-label">date:</label>
            <input id="buy_date" type="textarea" class="form-control input-sm">
        </div>
        <div class="form-group">
            <label class="control-label">reason:</label>
            <input id="buy_reason" type="textarea" class="form-control">
        </div>
        <input type="button" class="btn btn-default" value="Submit" onclick="updateBuyData()" >
        </form>
    </div>

    <div id="table"></div>

    <script type="text/javascript">

        $(document).ready( function(){
            // ページ読み込み時にDBからデータを取得
            readData();

            // 今日の日付をいれる
            today = getTheDateOfToday();
            $("#buy_date").val(today);
        });
        var getTheDateOfToday = function () {
            // 買い入力欄に日付をセット
            var now = new Date();
            var yyyymmdd = now.getFullYear() + "/" +
                           ( "0"+( now.getMonth()+1 ) ).slice(-2) + "/" +
                           ( "0"+now.getDate() ).slice(-2);
            return yyyymmdd;
        }
        var readData = function () {
            // 初期化
            deleteTableData();

            /* webを表示したときにデータを問い合わせる */
            /* 買いも売りもデータをすべて取得して順にテープルを作る*/
            $.getJSON(
                "./data" ,
                function(data) {
                    console.log(data);

                    for (var buy_idx = data.length - 1 ; buy_idx > -1; buy_idx--) {
                        var buy = data[buy_idx].buy;
                        var sell = data[buy_idx].sell;
                        var p_l = data[buy_idx].p_l;
                        
                        addTable(buy.id, buy.code, buy.price, buy.count, buy.date, buy.reason);
                        for (var sell_idx = 0; sell_idx < sell.length; sell_idx++) { 
                            addRow("sell", buy.id, sell[sell_idx].price, sell[sell_idx].count, sell[sell_idx].date, sell[sell_idx].reason);
                        }
                        addRow("p_l", buy.id, p_l.price, p_l.remain_count, "-", "-");
                    }
                });
        };
        var deleteTableData = function() {
            $("#table").empty();
        };
        var updateBuyData = function () {
            var code = $("#code").val();
            var price = $("#buy_price").val();
            var count = $("#buy_count").val();
            var date = $("#buy_date").val();
            var reason = $("#buy_reason").val();
            var resObj = sendBuyData(code, price, count, date, reason);

            if (resObj != null)
            {
                readData()
            }
        };
        var sendBuyData = function (code, price, count, date, reason) {
            $.ajax({
                type  : "GET",
                url   : "./buy",
                async : false,
                data  :
                {
                    "code" : code,
                    "price" : price,
                    "count" : count,
                    "date" : encodeURI(date),
                    "reason" : reason
                },
                success : function (data) {
                },
                error : function (data) {
                }
                });
            return true;
        };
        var addTable = function (buyId, code, price, count, date, reason) {
            //var tableTitle = $("<h2></h2>").text("Code: " + code);
            var tableHTML = $("<table></table>", { 
                                id    : "buy_table_" + buyId,
                                class : "table table-striped table-borderd table-responsive table-condensed"
                                });
            var tableHEAD = $("<thead></thead>")
                                .append($("<tr></tr>")
                                    .append($("<th></th>").text("Kind"))
                                    .append($("<th></th>").text("Price"))
                                    .append($("<th></th>").text("Count"))
                                    .append($("<th></th>").text("Date"))
                                    .append($("<th></th>").text("Reason"))
                                );
            var tableBODY = $("<tbody></tbody>")
                                .append($("<tr></tr>")
                                    .append($("<td></td>").append($("<b></b>").text("Buy")))
                                    .append($("<td></td>").text(price))
                                    .append($("<td></td>").text(count))
                                    .append($("<td></td>").text(date))
                                    .append($("<td></td>").text(reason))
                                );
            tableHTML.append(tableHEAD).append(tableBODY);

            var tableForm = $("<form></form>", { class: "form-inline" })
                                .append($("<b></b>", { class : "form-control-static" }).text("Sell:"))
                                .append($("<div></div>", { class : "form-group" })
                                            .append($("<label></label>", { class : "control-label" }).text("price:"))
                                            .append($("<input></input>", { class : "form-control input-sm" ,
                                                                           id    : "sell_price_" + buyId ,
                                                                           type  : "textarea"})))
                                .append($("<div></div>", { class : "form-group" })
                                            .append($("<label></label>", { class : "control-label" }).text("count:"))
                                            .append($("<input></input>", { class : "form-control input-sm" ,
                                                                           id    : "sell_count_" + buyId ,
                                                                           type  : "textarea"})))
                                .append($("<div></div>", { class : "form-group" })
                                            .append($("<label></label>", { class : "control-label" }).text("date:"))
                                            .append($("<input></input>", { class : "form-control input-sm" ,
                                                                           id    : "sell_date_" + buyId ,
                                                                           type  : "textarea",
                                                                           value : getTheDateOfToday()})))
                                .append($("<div></div>", { class : "form-group" })
                                            .append($("<label></label>", { class : "control-label" }).text("reason:"))
                                            .append($("<input></input>", { class : "form-control" ,
                                                                           id    : "sell_reason_" + buyId ,
                                                                           type  : "textarea"})))
                                .append($("<input></input>", { class : "btn btn-default" ,
                                                               value : "Submit",
                                                               onclick: "updateSellData(" + buyId + ")" }))
                                ;

            var panelHead = $("<div></div>", { class : "panel-heading" })
                            .append($("<h2></h2>", { class : "panel-title" }).text("Code: " + code));
            var panelBody = $("<div></div>", { class : "panel-body" })
                            .append(tableHTML);
            var panelFooter = $("<div></div>", { class : "panel-footer" })
                            .append(tableForm);
            var panel  = $("<div></div>", { class : "panel panel-default" })
                            .append(panelHead)
                            .append(panelBody)
                            .append(panelFooter);

            $("#table").append(panel);
        };
        var updateSellData = function (buyId) {
            var price = $("#sell_price_" + buyId).val();
            var count = $("#sell_count_" + buyId).val();
            var date = $("#sell_date_" + buyId).val();
            var reason = $("#sell_reason_" + buyId).val();
            var resObj = sendSellData(buyId, price, count, date, reason);

            if (resObj != null) {
                readData()
            }
        };
        var sendSellData = function (buyId, price, count, date, reason) {
            $.ajax({
                type  : "GET",
                url   : "./sell",
                async : false,
                data  :
                {
                    "buy_id" : buyId,
                    "price" : price,
                    "count" : count,
                    "date" : encodeURI(date),
                    "reason" : reason
                },
                success: function(data) {
                },
                error : function(data) {
                }
                });
            return true;
        };
        var addRow = function (kind, buyId, price, count, date, reason) {
            var rowHTML = $("<tr></tr>")
                          .append($("<td></td>").append($("<b></b>").text(kind)))
                          .append($("<td></td>").text(price))
                          .append($("<td></td>").text(count))
                          .append($("<td></td>").text(date))
                          .append($("<td></td>").text(reason))
            $("#buy_table_" + buyId + " tbody > tr:last").after(rowHTML);
        };
    </script>
    </div>
</body>

</html>
