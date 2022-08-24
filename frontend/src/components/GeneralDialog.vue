<template>
    <i class="fa fa-qq" aria-hidden="true"></i>
    <Dialog :options="{ title: data.title }" v-model="open">
        <template #body-content>
            <p class="text-gray-600">{{ data.message }}
            </p>
            <div class="flex mt-5">
                <Button @click="open = false" class="ml-auto"> Cancel </Button>
                <Button appearance="primary" :iconLeft="data.buttonIcon" class="ml-4" @click="$resources.method.submit()"
                    :loading="$resources.method.loading">
                    {{ data.buttonMessage }}
                </Button>
            </div>
        </template>
    </Dialog>
</template>
<script>
import { Dialog, Input } from 'frappe-ui'

export default {
    name: 'GeneralDialog',

    components: {
        Dialog,
        Input,
    },

    props: {
        modelValue: {
            type: Boolean,
            required: true,
        },
        entities: {
            type: Array,
            required: true,
        },
        for: {
            type: String,
        },
    },

    emits: ['update:modelValue', 'success'],

    computed: {
        data() {
            const items = this.entities.length === 1 ? `${this.entities.length} item` : `${this.entities.length} items`
            switch (this.for) {
                case 'unshare':
                    return {
                        title: "Remove?",
                        message: "Selected items will not be shared with you anymore.",
                        buttonMessage: "Remove",
                        buttonIcon: "trash-2",
                        methodName: "drive.api.files.unshare_entities"
                    }
                case 'restore':
                    return {
                        title: "Restore Items?",
                        message: "Selected items will be restored to their original locations.",
                        buttonMessage: "Restore",
                        buttonIcon: "refresh-ccw",
                        methodName: "drive.api.files.remove_or_restore"
                    }
                case 'remove':
                    return {
                        title: "Move to Trash?",
                        message: items + " will be moved to Trash. Items in Trash are deleted forever after 30 days.",
                        buttonMessage: "Move to Trash",
                        buttonIcon: "trash-2",
                        methodName: "drive.api.files.remove_or_restore"
                    }
            }
        },
        open: {
            get() {
                return this.modelValue
            },
            set(value) {
                this.$emit('update:modelValue', value)
            },
        },
    },

    resources: {
        method() {
            return {
                method: this.data.methodName,
                params: {
                    entity_names: JSON.stringify(
                        this.entities.map((entity) => entity.name)
                    ),
                },
                onSuccess(data) {
                    this.$emit('success', data)
                },
                onError(error) {
                    if (error.messages) {
                        console.log(error.messages);
                    }
                },
            }
        },
    },
}
</script>