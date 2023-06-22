<script setup>

let email = ref('testYhast@gmail.com')
let password = ref('testYhast1234')
let url = ref('')
let errors = ref([])
let comments = ref([
    {
        "id": 1166,
        "author": "Martin Crowleyout of network3rd+",
        "comment": "Great share right hereAwais Khan!!",
        "vader_neg": 0,
        "vader_neu": 0.304,
        "vader_pos": 0.696,
        "vader_compound": 0.7835,
        "roberta_neg": 0.0015315954806283116,
        "roberta_neu": 0.03658103197813034,
        "roberta_pos": 0.9618873596191406
    },
    {
        "id": 1167,
        "author": "Awais KhanAuthor",
        "comment": "Cheers Martin!",
        "vader_neg": 0,
        "vader_neu": 0.228,
        "vader_pos": 0.772,
        "vader_compound": 0,
        "roberta_neg": 0.002709739375859499,
        "roberta_neu": 0.06812034547328949,
        "roberta_pos": 0.9291698932647705
    },
    {
        "id": 1168,
        "author": "Alex Colhounout of network3rd+",
        "comment": "Love this!",
        "vader_neg": 0,
        "vader_neu": 0.182,
        "vader_pos": 0.818,
        "vader_compound": 0.6696,
        "roberta_neg": 0.0032275826670229435,
        "roberta_neu": 0.01796177588403225,
        "roberta_pos": 0.9788106679916382
    },
    {
        "id": 1169,
        "author": "Awais KhanAuthor",
        "comment": "Thanks for reading Alex!",
        "vader_neg": 0,
        "vader_neu": 0.484,
        "vader_pos": 0.516,
        "vader_compound": -0.4926,
        "roberta_neg": 0.0012925678165629506,
        "roberta_neu": 0.031280942261219025,
        "roberta_pos": 0.9674264788627625
    },
    {
        "id": 1170,
        "author": "Rhan Roblesout of network3rd+",
        "comment": "Thanks for sharing 🙏",
        "vader_neg": 0,
        "vader_neu": 0.149,
        "vader_pos": 0.851,
        "vader_compound": 0.6908,
        "roberta_neg": 0.002015003003180027,
        "roberta_neu": 0.04936650022864342,
        "roberta_pos": 0.9486185312271118
    },

])
let showComments = ref(false)
let loading = ref(false)
let loadingtext = ref('')


async function submitForm() {
    errors.value = []
    comments.value = []
    loading.value = true
    loadingtext.value = 'pleas wait ...'
    setTimeout(() => {
        loadingtext.value = 'Finding comments ...'
    }, 2000);
    await $fetch('http://127.0.0.1:8002/api/v1/post/add/', {
        method: 'POST',
        body: {
            url: url.value,
            email: email.value,
            password: password.value,
        }
    }).then(res => {
        loadingtext.value = 'processing comments ...'
        getCommentUrl()

    }).catch(err => {
        if (err.response) {
            for (const property in err.response._data) {
                errors.value.push(`${property}:${err.response._data[property]}`)
            }
        } else if (err.message) {
            errors.value.push('something went wrong')
        }

    })

}


async function getCommentUrl() {
    await $fetch('http://127.0.0.1:8002/api/v1/post/commentsMined?url=' + url.value + '&utm_source=share&utm_medium=member_desktop')
        .then(res => {
            loading.value = false
            comments.value = res?.comments
            showComments.value = true
        })

}
</script>


<template>
    <div class="py-10 px-6 bground">
        <div class=" w-1/2 mx-auto py-10 px-6 bg-white rounded-md shadow-md">
            <h1 class="mb-6 text-2xl capitalize">Find comments by url</h1>

            <form @submit.prevent="submitForm">
                <input v-model="email" type="email" placeholder="your email addres" class=" w-full mb-4 p-6 rounded-xl">
                <input v-model="password" type="password" placeholder="your password " class=" w-full mb-4 p-6 rounded-xl">
                <input v-model="url" type="url" required placeholder="post url" class=" w-full mb-4 p-6 rounded-xl">
                <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 text-white rounded-xl">
                    <p v-for="error in errors" :key="error">
                        {{ error }}
                    </p>
                </div>
                <div class="flex justify-between mt-5">
                    <NuxtLink to="/getCommentByUrl" class="nuxtlink py-4 px-6  rounded-md">show your urls</NuxtLink>
                    <button class="py-4 px-6  rounded-md">submit</button>
                </div>
            </form>
        </div>
        <div v-if="loading" class="flex gap-2 justify-center mt-10 text-white align-middle">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                width="60px" viewBox="0 0 100 100"
                preserveAspectRatio="xMidYMid">
                <circle cx="50" cy="50" r="32" stroke-width="8" stroke="#eae9e9cd"
                    stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" dur="1s" repeatCount="indefinite"
                        keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
                </circle>
                <circle cx="50" cy="50" r="23" stroke-width="8" stroke="#fff"
                    stroke-dasharray="36.12831551628262 36.12831551628262" stroke-dashoffset="36.12831551628262" fill="none"
                    stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" dur="1s" repeatCount="indefinite"
                        keyTimes="0;1" values="0 50 50;-360 50 50"></animateTransform>
                </circle>
            </svg>
            <p class="my-auto text-xl">{{ loadingtext }}</p>
        </div>

        <table class="border my-10 w-full shadow-md " v-if="showComments">
            <thead>
                <tr>
                    <th class="th-head">
                        row
                    </th>
                    <th class="th-head">
                        Title
                    </th>
                    <th class="th-head">
                        Comment
                    </th>
                    <th class="th-head">
                        VADER negative
                    </th>
                    <th class="th-head">
                        VADER neutral
                    </th>
                    <th class="th-head">
                        VADER positive
                    </th>
                    <th class="th-head">
                        VADER COMPOUND
                    </th>
                    <th class="th-head">
                        ROBERTA negative
                    </th>
                    <th class="th-head">
                        ROBERTA neutral
                    </th>
                    <th class="th-head">
                        ROBERTA positive
                    </th>
                </tr>

            </thead>
            <tbody>
                <tr v-for="(comment, index) in comments" :key="index">
                    <td class="px-6 py-4 ">
                        <div>{{ index + 1 }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.author }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.comment }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.vader_neg }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.vader_neu }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ comment?.vader_pos }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div
                            :class="comment?.vader_compound > 0 ? 'text-green-700' : comment?.vader_compound < 0 ? 'text-rose-500' : 'text-black'">
                            {{ comment?.vader_compound }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_neg).toFixed(2) }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_neu).toFixed(2) }}</div>
                    </td>
                    <td class="px-6 py-4 ">
                        <div>{{ (comment?.roberta_pos).toFixed(2) }}</div>
                    </td>

                </tr>

            </tbody>
        </table>

    </div>
</template>

<style scoped>
.bground {
    background: linear-gradient(-45deg, #eae9e9cd, #9a3ce7, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 10s ease infinite;
    min-height: 100vh;
    height: 100%;
}

table {
    display: block;
    border-radius: 0.375rem;
    overflow: hidden;
    background: rgba(216, 216, 216, 0.347);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: rgb(0, 0, 0)
}

.th-head {
    padding: 18px;
    font-size: 16px;
    color: rgb(255, 255, 255);
}

tbody tr {
    transition: 0.5s;
}

thead {
    background-color: #097853;

}

tbody tr:hover {
    background: #efeeee4d;
}

button:focus,
.nuxtlink:focus {
    outline: none;
}

input:focus {
    outline: none;
    background: linear-gradient(white, white) padding-box,
        linear-gradient(to right, rgb(0, 139, 23), darkorchid) border-box;
    border: 2px solid transparent; 

}

input {
    border: 2px solid rgba(255, 255, 255, 0);
    box-shadow: 0 4px 7px 0 rgba(10, 208, 53, 0.2);
}

input::placeholder {
    color: black;
    opacity: .5;
}

button,
.nuxtlink {
    background-color: #097853;
    border-radius: 8px;
    box-shadow: 0 4px 7px 0 rgba(19, 21, 19, 0.2);
    color: white;

}

@keyframes gradient {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}
</style>    