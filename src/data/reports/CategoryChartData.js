export const getPieChartData = (themes) => ({
  labels: ['Corporate Customer', 'PIC', 'Product', 'Account Manager'],
  datasets: [{
    label: 'Chatbot By Catgory',
    backgroundColor: [themes.primary, themes.warning, themes.danger, themes.success],
    data: [2478, 5267, 734, 1233],
  }],
})
