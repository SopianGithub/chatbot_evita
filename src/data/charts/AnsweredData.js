import { hex2rgb } from '../../services/vuestic-ui'

const generateYLabels = () => {
  const flip = !!Math.floor(Math.random() * 2)
  return flip ? ['Anwered', 'Not Answered'] : ['Not Answered', 'Anwered']
}

let generatedData
const firstCatIndex = 0

export const getLineAnsweredData = (themes, dataAns = [], dataNotAns = []) => {
  const size = 4
  const category = ['Corporate Customer', 'Account Manager', 'Product', 'PIC']
  const yLabels = ['Anwered', 'Not Answered']
  // console.log(dataAns)
  generatedData = {
	  labels: category.splice(firstCatIndex, 4),
	  datasets: [
	    {
	      label: yLabels[0],
	      backgroundColor: hex2rgb(themes.primary, 0.6).css,
	      borderColor: 'transparent',
	      data: [dataAns[0], dataAns[1], dataAns[2], dataAns[3]],
	    },
	    {
	      label: yLabels[1],
	      backgroundColor: hex2rgb(themes.info, 0.6).css,
	      borderColor: 'transparent',
	      data: [dataNotAns[0], dataNotAns[1], dataNotAns[2], dataNotAns[3]],
	    },
	  ],
  }

  return generatedData
}
