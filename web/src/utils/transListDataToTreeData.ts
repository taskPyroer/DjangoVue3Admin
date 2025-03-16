// 递归: 封装一个函数:将列表list数据转换成数据树形数据=>递归
// 遍历树形 有一个重点 要先找一个头
export function toArrayTree(list: any) {
    const treeList: any = []
    const map = {}
    // 遍历list数组，加入一个对象里面，id作为key.数组的item作为value
    list.forEach( (item: any) => {
        map[item.id] = item
        item.children = []
    })
    // 再次遍历list数组，如果map对象id与pid匹配成功，添加至item.children里面，反之，添加到treeList里面
    list.forEach( (item: any) => {
        if (map[item.parent]) {
            map[item.parent].children.push(item)
        } else {
            treeList.push(item)
        }
    })
    return treeList
}