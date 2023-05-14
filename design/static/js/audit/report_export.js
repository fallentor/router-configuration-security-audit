$(document).ready(function() {

	// 展示按钮事件
	$(".export-show-btn").click(function(event) {

		// 阻止默认行为
        event.preventDefault();

        // 获取data-id的值
        var device_id = $(this).attr('data-id');

        $('#id-input').val(device_id);
        $('#show-form').submit();
	});

	// 删除按钮事件
	$(".delete-btn").click(function(event) {

		// 阻止默认行为
		event.preventDefault();

		var device_id = $(this).attr('data-id');

		// 构造JSON对象
        var postData = {'device_id': device_id};

		// 弹出确认删除提示框
    	$('#confirm-delete-modal').modal('show');

    	// 确认删除按钮按下时的操作
		$('#confirm-delete-btn').click(function() {
			// 弹出确认删除提示框
    		$('#confirm-delete-modal').modal('hide');

			// 发送AJAX POST请求
	        $.ajax({
	            url: $("#delete-form").attr("action"),
	            type: 'POST',
	            data: postData,
	            success: function(data) {
	              	// 成功删除后的处理逻辑
	            	alert("删除成功");
	            	
	            	// 刷新当前页面以立即反映删除结果
            		location.reload();
	            },
	            error: function() {
	              alert('删除失败');
	            }
	        });
		});

	});
		
})