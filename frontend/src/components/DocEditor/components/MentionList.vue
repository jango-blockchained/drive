<template>
  <div>
    <div
      v-if="items.length"
      class="min-w-40 rounded-lg border bg-surface-white p-1.5 text-base shadow-lg"
    >
      <button
        v-for="(item, index) in items"
        :key="index"
        :class="[
          index === selectedIndex ? 'bg-surface-gray-2' : 'text-ink-gray-9',
          'flex w-full items-center whitespace-nowrap rounded p-1 text-sm',
        ]"
        @click="selectItem(index)"
        @mouseover="selectedIndex = index"
      >
        <Avatar
          size="sm"
          class="mr-1"
          :label="item.label"
          :image="item.user_image"
        />
        {{ item.label }}
      </button>
    </div>
  </div>
</template>

<script>
import { Avatar } from "frappe-ui"
export default {
  components: {
    Avatar,
  },
  props: {
    items: {
      type: Array,
      required: true,
    },
    command: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      selectedIndex: 0,
    }
  },
  computed: {
    currentUserName() {
      return this.$store.state.user.id
    },
  },
  watch: {
    items() {
      this.selectedIndex = 0
    },
  },
  methods: {
    onKeyDown({ event }) {
      if (event.key === "ArrowUp") {
        this.upHandler()
        return true
      }
      if (event.key === "ArrowDown") {
        this.downHandler()
        return true
      }
      if (event.key === "Enter") {
        this.enterHandler()
        return true
      }
      return false
    },
    upHandler() {
      this.selectedIndex =
        (this.selectedIndex + this.items.length - 1) % this.items.length
    },
    downHandler() {
      this.selectedIndex = (this.selectedIndex + 1) % this.items.length
    },
    enterHandler() {
      this.selectItem(this.selectedIndex)
    },
    selectItem(index) {
      const item = this.items[index]
      if (item) {
        this.command({
          id: item.value,
          label: item.label,
          author: this.currentUserName,
          type: item.type,
        })
      }
    },
  },
}
</script>

<style>
.item {
  display: block;
  margin: 0;
  width: 100%;
  text-align: left;
  background: transparent;
  border-radius: 0.4rem;
  border: 1px solid transparent;
  padding: 0.2rem 0.4rem;
}
.item.is-selected {
  border-color: #000;
}
</style>
