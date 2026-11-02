import {ElMessage} from "element-plus";

export function handleFileError(res: any, fileName: string) {
    const rawData = res?.data !== undefined ? res.data : res;
    if (rawData && rawData.type === 'application/json') {
        const reader = new FileReader();
        reader.onload = function() {
            try {
                const message = JSON.parse(reader.result as string).msg || '导出失败';
                ElMessage.error(message);
            } catch (e) {
                ElMessage.error('导出失败');
            }
        };
        reader.readAsText(new Blob([rawData]));
        return;
    }
    const blob = rawData instanceof Blob ? rawData : new Blob([rawData]);
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = downloadUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(downloadUrl);
}