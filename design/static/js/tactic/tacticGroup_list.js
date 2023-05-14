$(document).ready(function () {

    // 更新按钮点击事件
    $(".update-btn").click(function () {
      window.location.reload(); // 重新加载页面
    });


    // 删除按钮点击事件
    $(".delete-btn").click(function () {
        // 取消表单提交默认行为
        event.preventDefault();

        var tactic_remark_id = $('input[name="tactic_remark_select"]:checked').val();

        if (!tactic_remark_id) {
            alert('请先选择需要删除策略组');
            return;
        }

        // 弹出确认删除提示框
        $('#confirm-delete-modal').modal('show');
        

        $('#confirm-delete-btn').click(function() {
            // 隐藏确认删除提示框
            $('#confirm-delete-modal').modal('hide');

            $.ajax({
                url: $('#delete-form').attr('action'),
                method: "post",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}",
                    tactic_remark_id: tactic_remark_id,
                },
                success: function (response) {
                    // 显示删除成功提示
                    alert('删除成功');
                    
                    // 删除后重载页面
                    window.location.reload();
                },
                error: function(response) {
                    // 删除失败，输出错误信息
                    alert('删除失败：' + response.error);
                }
            });
        });
    });
})