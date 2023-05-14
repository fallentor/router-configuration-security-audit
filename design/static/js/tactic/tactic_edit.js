// ajax 处理修改按钮
$(function() {
	$('#edit-form').on('submit', function(event) {
    	event.preventDefault();
    	
    	// 禁用提交按钮
    	var submit_button = $('#edit_button');
    	submit_button.prop('disabled', true).html('修改中...');
		
		$.ajax({
			url: $('#edit-form').attr('action'),
			method: "post",
			data: $(this).serialize(),

			success: function(response) {
				if (response.status === 'success') {
					showSuccess(response.msg);
				} else {
					showError(response.msg);
				}
			},

			error: function(xhr, status, error) {
		        showError('服务器通信错误，请联系管理员！');
		    },

		    complete: function() {  
	        	// 重新启用提交按钮
	        	submit_button.prop('disabled', false).html('修改');
		    }
		});
	});

	// 提示框显示一段时间后自动消失的函数
	function hideAlert(element) {
	    setTimeout(function() {
	      $(element).fadeOut();
	    }, 2000); // 2 秒后自动隐藏提示框
    }

    // 显示成功信息的提示框
  	function showSuccess(message) {
	    $('#success-msg').html(message);
	    $('#success-box').removeClass('d-none').addClass('show');// 修改为 Bootstrap Alert 组件
	    hideAlert('#success-box');
    }

    // 显示错误信息的提示框
  	function showError(message) {
    	$('#error-msg').html(message);
    	$('#error-box').removeClass('d-none').addClass('show');// 修改为 Bootstrap Alert 组件
    	hideAlert('#error-box');
  	}

});