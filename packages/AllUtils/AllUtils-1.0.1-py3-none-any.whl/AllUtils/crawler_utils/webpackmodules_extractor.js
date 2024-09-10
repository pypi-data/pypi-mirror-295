const fs = require('fs');

function A_toStringArray(modulesArray) {
    // 使用map方法遍历数组，将函数转换为字符串，未定义的元素保持为未定义
    var stringArray = modulesArray.map(function (item) {
        if (typeof item === 'function') {
            return item.toString();
        } else {
            return undefined;
        }
    });
    return stringArray;
}

function handleUndefined(value) {
    return value !== undefined ? value : 'undefined';
}

function A_save_to_txt(modules_array, file_path_name) {
    // 将模块数组保存为txt文件

    if (!file_path_name.endsWith('.txt')) {
        file_path_name += '.txt';
    }
    // 将模块数组保存为txt文件
    var arrayAsString = modules_array.join(',');
    // console.log(arrayAsString)
    // 将字符串写入到文本文件中,并在第一行添加"["，在最后一行添加"]"在第一行添加"["，在最后一行添加"]"
    arrayAsString = '[' + arrayAsString + ']'
    fs.writeFileSync(file_path_name, arrayAsString, 'utf-8');
    console.log(`保存成功，文件路径为：${file_path_name}`);
}

function save_to_json(modules_array, file_path_name) {
    // 将模块数组保存为json文件
    const jsonMethods = JSON.stringify(modules_array);
    fs.writeFileSync(file_path_name, jsonMethods, 'utf-8');
    console.log(`保存成功，文件路径为：${file_path_name}`);
}

function load_from_json(file_path_name) {
    // 从json文件加载模块数组
    const jsonMethods = fs.readFileSync(file_path_name, 'utf-8');
    const methodsArray = JSON.parse(jsonMethods);
    return methodsArray;
}

function A_get_modules_num_array(regexPattern, string) {
    var matchArray = [];
    var match;

    while ((match = regexPattern.exec(string)) !== null) {
        var number = parseInt(match[0].match(/\d+/)[0], 10); // 提取匹配的整数并转换为整数类型
        matchArray.push(number);
    }
    return matchArray;
}

function A_findExtraElements(array1, array2) {
    return array1.filter(item => !array2.includes(item));
}

function A_restore_modules(modules_array, used_module_index_array) {
    // 还原模块数组，将未使用的模块设置为undefined
    "该函数需要传入包含全部webpack模块的数组、逆向得到的解密/加密所用到的全部模块的index(包括模块间的调用关系)"
    "返回值为还原后的模块数组,调用模块的索引不需要发生变化"
    console.log(used_module_index_array)
    var new_modules_array = modules_array.map(function (item, index) {
        if (used_module_index_array.includes(index)) {
            return item;
        } else {
            return '';
        }
    });
    return new_modules_array;
}

function A_extract_webpack_modules_index(modules_array, target_module_index_array, search_word) {
    // search_word: 每个模块调用其他模块时使用的储存启动器的变量名
    "该函数需要传入包含全部webpack模块的数组、逆向得到的解密/加密所用到的全部基本模块（不考虑模块间的调用关系）的index、模块之间用于相互调用的变量名（储存了启动器的变量名）"
    "返回值为逆向得到的解密/加密所用到的全部模块的index（包括模块间的调用关系）"
    var modules_string_array = A_toStringArray(modules_array)
    var regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(\\d+\\)`, 'g');
    var next = target_module_index_array;
    var cur = [];
    var real_next = A_findExtraElements(next, cur)

    while (real_next.length > 0) {
        next = []
        real_next.forEach(function (item) {
            cur.push(item)
            next = next.concat(A_get_modules_num_array(regexPattern, modules_string_array[item]))
            // console.log(`cur: ${cur}`, `next: ${next}`, `item: ${item}`, `real_next: ${real_next}`)
        })
        real_next = A_findExtraElements(next, cur)
    }
    used_module_index_array = [...new Set(cur)];
    return used_module_index_array;
}

function O_get_modules_name_array(string, search_word, mode = 'n', string_use = 'n') {
    "该函数需要传入字符串、模块之间用于相互调用的变量名、对象的属性是以数字还是字母命名、属性名称是否使用引号"
    var matchArray = [];
    var match;
    var contentInBrackets;
    var regexPattern;
    if (mode === 'n') {
        if (string_use === 'n') {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(\\d+\\)`, 'g')
        } else {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(['"]\\d+['"]\\)`, 'g')
        }
        while ((match = regexPattern.exec(string)) !== null) {
            var number = match[0].match(/\d+/)[0]; // 提取匹配的整数并转换为整数类型
            matchArray.push(number);
        }
    } else if (mode === 's') {
        if (string_use === 'n') {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(([a-zA-Z]+)\\)`, 'g')
        } else {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(['"]([a-zA-Z]+)['"]\\)`, 'g')
        }
        while ((match = regexPattern.exec(string)) !== null) {
            contentInBrackets = match[1]; // 提取括号中的内容
            matchArray.push(contentInBrackets);
        }
    } else {
        if (string_use === 'n') {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(([a-zA-Z0-9_/+=]+)\\)`, 'g')
        } else {
            regexPattern = new RegExp(`(?<![a-zA-Z])${search_word}\\(['"]([a-zA-Z0-9_/+=]+)['"]\\)`, 'g')
        }
        while ((match = regexPattern.exec(string)) !== null) {
            contentInBrackets = match[1]; // 提取括号中的内容
            matchArray.push(contentInBrackets);
        }
    }
    return matchArray;
}

function O_extract_webpack_modules_index(modules_object, target_module_name_array, search_word_array, mode = 'n', use_string = 'n') {
    // search_word: 每个模块调用其他模块时使用的储存启动器的变量名
    "该函数需要传入包含全部webpack模块的对象、逆向得到的解密/加密所用到的全部基本模块（不考虑模块间的调用关系）的名称、模块之间用于相互调用的变量名（储存了启动器的变量名）"
    "返回值为逆向得到的解密/加密所用到的全部模块的名称（包括模块间的调用关系）"
    var modules_array = Object.values(modules_object);
    target_module_name_array = target_module_name_array.map(String)
    var next = target_module_name_array;
    var cur = [];
    var real_next = A_findExtraElements(next, cur)
    while (real_next.length > 0) {
        next = []
        // console.log(real_next)
        real_next.forEach(function (item) {
            cur.push(item)
            var tmp = item
            // console.log(tmp, modules_object[tmp])
            search_word_array.forEach(function (item) {
                try {
                    // console.log(modules_object[tmp].toString(), item, mode)
                    next = next.concat(O_get_modules_name_array(modules_object[tmp].toString(), item, mode, use_string))
                    // console.log(next)
                } catch (error) {
                    error.message = `模块 ${tmp} 不存在,可能因为 实际模块 xxx 被映射为了 ${tmp} ，请检查webpack中的映射关系`
                    console.error(error)
                    throw error
                }
            });
        })
        real_next = A_findExtraElements(next, cur)
    }
    used_module_name_array = [...new Set(cur)];
    return used_module_name_array;
}

function O_restore_modules(modules_object, used_module_name_array) {
    console.log(used_module_name_array)
    // console.log(modules_object)
    let new_modules_object = {}
    used_module_name_array.forEach(function (item) {
        new_modules_object[item] = modules_object[item]
    })
    // console.log(new_modules_object)
    return new_modules_object;
}

function O_save_to_txt(modules_object, file_path_name) {
// 将模块对象保存为txt文件
    function functionStringifier(key, value) {
        if (typeof value === 'function') {
            return value.toString(); // 将函数转换为字符串
        }
        return value;
    }

    const objStr = JSON.stringify(modules_object, functionStringifier, 4);

    // 处理函数字符串，去除引号
    const processedObjStr = objStr.replace(/"function/g, 'function').replace(/}"/g, '}').replace(/\\r\\n/g, '\n    ');
    fs.writeFileSync(file_path_name, processedObjStr);

    console.log(`保存成功，文件路径为：${file_path_name}`);
}


module.exports = {
    A_extract_webpack_modules_index,
    A_restore_modules,
    A_save_to_txt,
    A_findExtraElements,
    O_extract_webpack_modules_index,
    O_restore_modules,
    O_save_to_txt
}
aaa = {
    '1': function () {
        console.log('1');
        n('2');
        n('3')
    }, '2': function () {
        console.log('2');
        n('4');
        n('5');
        n('3')
    }, '3': function () {
        console.log('3')
    }, '4': function () {
        console.log('4')
    }, '5': function () {
        console.log('5')
    }, '6': function () {
        console.log('6')
    }, '7': function () {
        console.log('7')
    }, '8': function () {
        console.log('8')
    }, '9': function () {
        console.log('9')
    }, '10': function () {
        console.log('10')
    }
}
name = (O_extract_webpack_modules_index(aaa, ['1'], ['n'], 'n', 's'))
console.log(name)
mudules = O_restore_modules(aaa, name)
console.log(mudules)
O_save_to_txt(mudules, 'test.txt')