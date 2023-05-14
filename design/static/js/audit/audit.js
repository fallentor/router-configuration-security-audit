$(document).ready(function () {

	// 查看/修改按钮点击事件
    $(".export-btn").click(function (event) {

    	// 取消表单提交默认行为
        event.preventDefault();

        // 获取当前的按钮对应的 data-id 值
        var device_id = $(this).attr("data-id");

        $('#id-input').val(device_id);
        $('#export-form').submit();

    });

    // 绑定审计按钮点击事件
    $('.audit-btn').click(function(event) {

        // 取消表单提交默认行为
        event.preventDefault();

        // 获取data-id的值
        var deviceId = $(this).attr('data-id');

        // 构造JSON对象
        var postData = {'device_id': deviceId};
        
        // 发送AJAX POST请求
        $.ajax({
            url: $("#audit-form").attr("action"),
            type: 'POST',
            data: postData,
            success: function(data) {
              if (data.success) {
                alert('审计成功！');

                // 刷新当前页面
                location.reload();
                
              } else {
                alert('审计失败！');
              }
            },
            error: function(xhr, status, error) {
              alert('审计请求失败！');
            }
        });
    });

})