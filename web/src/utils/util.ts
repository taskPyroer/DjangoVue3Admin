export function formatUnitSize(bytes, is_unit, fixed, end_unit) //字节转换，到指定单位结束 is_unit：是否显示单位  fixed：小数点位置 end_unit：结束单位
{
    if (bytes == undefined) return 0;

    if (is_unit == undefined) is_unit = true;
    if (fixed == undefined) fixed = 2;
    if (end_unit == undefined) end_unit = '';

    if (typeof bytes == 'string') bytes = parseInt(bytes);
    var unit = [' B', ' KB', ' MB', ' GB', 'TB'];
    var c = 1024;
    for (var i = 0; i < unit.length; i++) {
        var cUnit = unit[i];
        if (end_unit) {
            if (cUnit.trim() == end_unit.trim()) {
                var val = i == 0 ? bytes : fixed == 0 ? bytes : bytes.toFixed(fixed)
                if (is_unit) {
                    return val + cUnit;
                } else {
                    val = parseFloat(val);
                    return val;
                }
            }
        } else {
            if (bytes < c) {
                var val = i == 0 ? bytes : fixed == 0 ? bytes : bytes.toFixed(fixed)
                if (is_unit) {
                    return val + cUnit;
                } else {
                    val = parseFloat(val);
                    return val;
                }
            }
        }

        bytes /= c;
    }
}
