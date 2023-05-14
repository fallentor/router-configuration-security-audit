// 添加按钮事件
// 获取添加按钮
const addBtn = document.getElementById("add-btn");
// 监听添加按钮点击事件
addBtn.addEventListener("click", function() {
    // 跳转到添加页面
    window.location.href = "/device/device_add/";
});

// 添加 confirm-delete-modal 显示时机
$('#delete-form').on('submit', function(event) {
    // 取消表单提交默认行为
    event.preventDefault();

    // 获取选中设备 ID
    var device_id = $('input[name="node"]:checked').val();

    if (!device_id) {
        alert('请先选择设备');
        return;
    }

    // 将取到的设备 ID 填充进 form 表单中
    $('#delete-device-id').val(device_id);

    // 弹出确认删除提示框
    $('#confirm-delete-modal').modal('show');
});

// 确认删除按钮按下时的操作
$('#confirm-delete-btn').click(function() {
    $('#confirm-delete-modal').modal('hide');
    // 提交表单并处理成功/失败情况
    $.ajax({
        url: $('#delete-form').attr('action'),
        type: 'POST',
        data: $('#delete-form').serialize(),
        success: function(response) {
            // 显示删除成功提示
            alert('删除成功');

            // 刷新当前页面以立即反映删除结果
            location.reload();
        },
        error: function(response) {
            // 删除失败，输出错误信息
            alert('删除失败：' + response.error);
        }
    });
});

// 搜索功能 
