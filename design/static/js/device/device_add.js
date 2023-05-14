// IP地址格式验证
function checkIp(ipInput) {
  var ipAddress = ipInput.value;
  var ipFormat = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
  if (ipAddress.match(ipFormat)) {
    var parts = ipAddress.split(".");
    for (var i = 0; i < 4; i++) {
      var part = parseInt(parts[i]);
      if (part < 0 || part > 255 || isNaN(part)) {
        showIpWarning("IP地址格式不正确");
        return false;
      }
    }
    hideIpWarning();
    return true;
  } else {
    showIpWarning("IP地址格式不正确");
    return false;
  }
}

function hideIpWarning() {
  var warningDiv = document.getElementById('ip_warning');
  warningDiv.classList.add('d-none');
}

function showIpWarning(warningMsg) {
  var warningDiv = document.getElementById('ip_warning');
  warningDiv.textContent = warningMsg;
  warningDiv.classList.remove('d-none');
}

// 检查时间格式是否正确
$('#last_checked').on('blur', function() {
  var input_val = $(this).val();
  var format = /^\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}$/;
  if (!format.test(input_val)) {
    $('#time_warning').removeClass('d-none');
  } else {
    $('#time_warning').addClass('d-none');
  }
});

// ajax 处理保存按钮
$(function() {
  $('#device-form').on('submit', function(event) {
    event.preventDefault();
  
    // 禁用提交按钮
    var submit_button = $('#save_button');
    submit_button.prop('disabled', true).html('保存中...');

    $.ajax({
      url: $('#device-form').attr('action'),
      method: "post",
      data: $(this).serialize(),

      success: function(response){
        if (response.status === "success") {
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
        submit_button.prop('disabled', false).html('保存');
      }
    });
  });

  // 提示框显示一段时间后自动消失的函数
  function hideAlert(element) {
    setTimeout(function() {
      $(element).fadeOut();
    }, 5000); // 5 秒后自动隐藏提示框
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
