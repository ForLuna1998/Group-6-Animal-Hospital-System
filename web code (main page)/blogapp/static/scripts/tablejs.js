$("table#aijquery").on("click","button.edit",function(){
    var $this=$(this);    //获取被点击的按钮
    var $tr=$this.parents("tr");    //获取当前按钮所在的tr行
    $tr.find("td").not($("td:has(button)")).each(function(){ //获取当前行所有除了含有button的td
        var $td=$(this);
        var _t=$td.text();
        var _w=$td.width();
        var _h=$td.height();
        $td.html("");
        var $input=$("<input type='text' class='border border-primary'>");
        $input.appendTo($td).width(_w).val(_t);
    });
    $this.removeClass().addClass("btn btn-danger btn-sm ajax").text("Submit");//更改按钮的样式
});
// http://www.aijquery.cn/Html/jqueryshili/108.html

$("table#aijquery").on("click","button.ajax",function(){
    var $this=$(this);
    var $tr=$this.parents("tr");
     
    //获取编辑后的内容，并放入一个数组内
    var v=[];
    $tr.find("td input:text").each(function(){
        v.push($(this).val());
    });
     
    //用jquery里post方法，把数据提交到后台，经过后台处理后，在输出到前台
    $.post("/Html/aijquery/ajax-post/",{"d":v},function(d){
        //获取到经过后台处理的数据，动态更新到前台
        var narray=d.split(",");
        var nhtml="<td>"+narray.join("</td><td>")+"</td>";
        nhtml=nhtml+"<td><button class=\"btn btn-primary btn-sm edit\">编辑</button></td>";
        $tr.html(nhtml);
    });
});
