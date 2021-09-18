import Vue from 'vue';
import Vuex from 'vuex';

const state = {
  fileArray: null,
};

const mutations = {
  reset(curState) {
    curState.fileArray = null;
  },
  init(curState, array) {
    curState.fileArray = array;
  },
};

Vue.use(Vuex);
export default new Vuex.Store({
  state,
  mutations,
});
