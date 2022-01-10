let generatedData

export const getProductChart = (themes, varlabel = ['North America', 'South America', 'Australia'], vardata = [2478, 5267, 734]) => {
  // if (generatedData) {
  //   generatedData.datasets[0].backgroundColor = [themes.danger, themes.info, themes.primary]
  // } else {
  const arrColor = [themes.danger, themes.info, themes.primary, themes.warning, themes.success]
  const bcColor = []
  for (var i = 0; i < vardata.length; i++) {
    if (i > arrColor.length) {
      bcColor[i] = arrColor[i - arrColor.length]
    } else {
      bcColor[i] = arrColor[i]
    }
  }

  generatedData = {
    labels: varlabel,
    datasets: [{
      label: 'Trend Product',
      backgroundColor: bcColor,
      data: vardata,
    }],
  }
  // }

  return generatedData
}
