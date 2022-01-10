export const getCategoryChart = (themes, labelArr = ['Corporate Customer', 'PIC', 'Product', 'Account Manager'], valArr = [2478, 5267, 734, 1233]) => ({
  labels: labelArr,
  datasets: [{
    label: 'Chatbot By Catgory',
    backgroundColor: [themes.primary, themes.info, themes.warning, themes.danger],
    data: valArr,
  }],
})
